#!/usr/bin/env python
# Prototype Stock Recs
import re
import twitter

from time import strftime
from datetime import date,timedelta
import pygtk
import gtk

# Login
api = twitter.Api(consumer_key='g5uq5QP3qzc4HncYPDFPlA',consumer_secret='UFaLPpT5d5mLGMFGc6KLZNWfj396EErHX7X1tqG6tc',access_token_key='18615161-4Pm3pAlPigqvd1SED8oykNnIKx3cf6fESjSr5b9NY',access_token_secret='x4wxVEQaucvvypJvrL3rugvbccRvgp898TbFxZzuORA')



class Base:
#twitter_search = twitter.Twitter(domain="search.twitter.com",api_version=none)
# Time frame 
	def analysis(self,ticker):
		delta_t = 7
		now = date.today()
		end_date = now - timedelta(days=delta_t)
		time_frame = 'since:' + str(end_date)

# Create adjectives and verbs which are assumed to be positive
		positive_words = ['buy\\b','highs?\\b','beats?\\b','new\\b','good\\b','great\\b','surprise\\b','higher profits?','profits? increase[a-z]*','exceed[a-z]* analysts? expectations?','impressive profitability','analysts? upgrade[a-z]*','bull[a-z]*\\b','launch[a-z]*\\b','revenues? higher','wins?\\b']
		negative_words = ['sell\\b','lows?\\b','down\\b','loss[a-z]*\\b','bad\\b','analysts? downgrade[a-z]*','low revenues?','bear[a-z]*\\b','low expectations?','loses?\\b','defaults?\\b','avoid\\b','sold\\b'] 
		
		# Sentiment Variables
		b_count = 0
		s_count = 0
		my_rec = 0 # total
		# Enter Stock Ticker
		ticker = '$' +ticker
		###########
		# STAGE 1 #
		###########
		sig1 = 'long'
		sig2 = 'short'
		stg1_count = 0
		for i in range(1,10):
			l_search = api.GetSearch('"'+sig1 +' '+ ticker + '"' +' ' +  time_frame + ' ',page=i,per_page=10)
			stg1_count += len(l_search)
			if len(l_search)==0:
				break
			else:
				b_count += len(l_search)

		for i in range(1,10):
			s_search = api.GetSearch('"'+sig2+' '+ticker +'"'+ ' '+time_frame+' ',page=i,per_page=10)
			stg1_count += len(s_search)
			if len(s_search)==0:
				break
			else:
				s_count += len(s_search)
		###########
		# STAGE 2 #
		###########
		stg2_count = 0
		new_delta_t = 2
		end_date = now - timedelta(days=new_delta_t)
		time_frame = 'since:' + str(end_date)

		###########
		stg1_2_count = 0
		for i in range(1,10):
			l_search = api.GetSearch('"'+sig1 +' '+ ticker + '"' +' ' +  time_frame + ' ',page=i,per_page=10)
			stg1_2_count += len(l_search)
			if len(l_search)==0:
				break

		for i in range(1,10):
			s_search = api.GetSearch('"'+sig2+' '+ticker +'"'+ ' '+time_frame+' ',page=i,per_page=10)
			stg1_2_count += len(s_search)
			if len(s_search)==0:
				break

		###########

		sent_score = 0
		count_pos = 0
		count_neg = 0
		# Extract tweets Loop
		for i in range(1, 10):
			b0_search = api.GetSearch(ticker + ' ' + time_frame + ' ' ,page=i,per_page=100) 
			if len(b0_search) == 0:
        			break
			else:
				stg2_count += len(b0_search)
				for f in b0_search:
					for w in positive_words:

						matchObj = re.search(w,f.text,re.I)
						if matchObj:
							count_pos += 1
					for w in negative_words:
						matchObj = re.search(w,f.text,re.I)
						if matchObj:
							count_neg += 1
		#############################
		# Calculate Sentiment Score #
		#############################
		my_rec = b_count - s_count # from stage 1
		sent_score = float(count_pos - count_neg)/float(stg2_count) # from stage 2
		sent_adj = float(float(delta_t-new_delta_t)/float(new_delta_t))*sent_score*(stg1_count - stg1_2_count) # adj stage 2 score
		my_rec = my_rec + .2*sent_adj
		##########
		# OUTPUT *
		##########
		if int(my_rec) > 5 :
			return ("BUY\n" + "\nPositive Recs: " + str(b_count) + "\tNegative Recs: " + str(s_count) + "\nPositive words: "+str(count_pos)+"\tNegative words: "+str(count_neg)+"\nAnalyst Overall Rec: " +str(b_count-s_count) + "\nSentiment Score: " + str(sent_score) + "\nAdjusted Score: " + str(my_rec) ) # Basic Recommendation
		elif int(my_rec) < -5 :
			return ("SELL\n" + "\nPositive Recs: " + str(b_count) + "\tNegative Recs: " + str(s_count) + "\nPositive words: "+str(count_pos)+"\tNegative words: "+str(count_neg)+"\nAnalyst Overall Rec: " +str(b_count-s_count) + "\nSentiment Score: " + str(sent_score) + "\nAdjusted Score: " + str(my_rec) ) # Basic Recommendation
		else:
			return ("HOLD\n" + "\nPositive Recs: " + str(b_count) + "\tNegative Recs: " + str(s_count) + "\nPositive words : "+str(count_pos)+"\tNegative words : "+str(count_neg)+"\nAnalyst Overall Rec : " +str(b_count-s_count) + "\nSentiment Score: " + str(sent_score) + "\nAdjusted Score: " + str(my_rec) ) # Basic Recommendation

	def destroy(self,widget,data=None):
		gtk.main_quit()

	def relabel(self,widget):
		self.label1.set_text("")
		self.textbox.set_text("")

	def textchange(self,widget):
		self.window.set_title(self.textbox.get_text())	
		q=self.textbox.get_text()
		self.label1.set_text("Loading ...")
		if len(q) >=1 :
			k=self.analysis(q)
			self.label1.set_text(k)
		else :
			self.label1.set_text("invalid entry")

	def __init__(self):
			

		self.window=gtk.Window(gtk.WINDOW_TOPLEVEL)
		self.window.set_position(gtk.WIN_POS_CENTER)

		self.window.set_size_request(300,450)
		self.window.set_title("My Morgan Challenge")
		self.button1=gtk.Button("EXIT")
			
		self.button1.connect("clicked",self.destroy)
		self.button1.set_tooltip_text("this button will close the window")
		
		self.textbox=gtk.Entry()
		self.textbox.set_max_length(5)

		self.button4=gtk.Button("Clear Result")
		self.button4.connect("clicked",self.relabel)


		self.button3=gtk.Button("Analysis")
		self.button3.connect("clicked",self.textchange)
			
		
		self.label1=gtk.Label("Results")
		self.label2=gtk.Label("Enter Ticker:       ")
		self.label3=gtk.Label("        ")
		self.label4=gtk.Label("                           ")
		self.label5=gtk.Label("             ")
		self.label6=gtk.Label("        ")
		self.label7=gtk.Label("        ")
		self.label8=gtk.Label("        ")
		self.label9=gtk.Label("        ")
		self.label10=gtk.Label("        ")

		self.pix=gtk.gdk.pixbuf_new_from_file("wol.png")
		self.image=gtk.image_new_from_pixbuf(self.pix)
		
		self.box1=gtk.HBox()
		self.box1.pack_start(self.image)
		
		self.box2=gtk.HBox()
		self.box2.pack_start(self.label3)
		self.box2.pack_start(self.label2)
		self.box2.pack_start(self.textbox)
		self.box2.pack_start(self.label4)

		self.box3=gtk.HBox()
		self.box3.pack_start(self.label5)
		self.box3.pack_start(self.button3)
		self.box3.pack_start(self.label6)
		
		self.box4=gtk.HBox()
		self.box4.pack_start(self.label1)

		self.box5=gtk.HBox()
		self.box5.pack_start(self.button4)
		self.box5.pack_start(self.button1)	

		self.box10=gtk.VBox()
		self.box10.pack_start(self.box1)
		self.box10.pack_start(self.box2)
		self.box10.pack_start(self.box3)
		self.box10.pack_start(self.box4)

		self.box10.pack_start(self.label7)
		self.box10.pack_start(self.box5)
		self.window.add(self.box10)
		
		self.window.show_all()
		self.window.connect("destroy", self.destroy)

	def main(self):
		gtk.main()
if __name__=="__main__":
	base=Base()
	base.main()

