import curses
from curses import wrapper
import time

#stdscr = curses.initscr()
#curses.noecho()

border_tl = ''
border_tr = ''
border_bl = ''
border_br = ''
border_hl = ''
border_vl = ''

border_tl_s = '┌'
border_tr_s = '┐'
border_bl_s = '└'
border_br_s = '┘'
border_hl_s = '─'
border_vl_s = '│'

border_tl_d = '╔'
border_tr_d = '╗'
border_bl_d = '╚'
border_br_d = '╝'
border_hl_d = '═'
border_vl_d = '║'



def draw_panel_borders(stdscr, activePanel = 1):
	#stdscr.clear()
	half_x = int(curses.COLS/2)

	top_border_y = 1
	bottom_border_y = curses.LINES-1-4

	if activePanel == 1:
		stdscr.insstr(top_border_y,0, '╔')
		stdscr.insstr(bottom_border_y,0, '╚')

		for x in range(1,half_x-1):
			stdscr.insstr(top_border_y,x, '═')
			stdscr.insstr(bottom_border_y,x, '═')


		for y in range(top_border_y+1,bottom_border_y):
			stdscr.insstr(y,0, '║')
			stdscr.insstr(y,half_x-1, '║')

		stdscr.insstr(top_border_y,half_x-1, '╗')
		stdscr.insstr(bottom_border_y,half_x-1, '╝')


		#---------------	
		stdscr.insstr(1,half_x, '┌')
		stdscr.insstr(bottom_border_y,half_x, '└')

		for x in range(half_x+1,curses.COLS-1):
			stdscr.insstr(1,x, '─')
			stdscr.insstr(bottom_border_y,x, '─')


		for y in range(1+1,bottom_border_y):
			stdscr.insstr(y,half_x, '│')
			stdscr.insstr(y,curses.COLS-1, '│')

		stdscr.insstr(1,curses.COLS-1, '┐')
		stdscr.insstr(bottom_border_y,curses.COLS-1, '┘')

	elif activePanel == 2:

		stdscr.insstr(top_border_y,0, '┌')
		stdscr.insstr(bottom_border_y,0, '└')

		for x in range(1,half_x-1):
			stdscr.insstr(top_border_y,x, '─')
			stdscr.insstr(bottom_border_y,x, '─')


		for y in range(top_border_y+1,bottom_border_y):
			stdscr.insstr(y,0, '│')
			stdscr.insstr(y,half_x-1, '│')

		stdscr.insstr(top_border_y,half_x-1, '┐')
		stdscr.insstr(bottom_border_y,half_x-1, '┘')


		#---------------	
		stdscr.insstr(1,half_x, '╔')
		stdscr.insstr(bottom_border_y,half_x, '╚')

		for x in range(half_x+1,curses.COLS-1):
			stdscr.insstr(1,x, '═')
			stdscr.insstr(bottom_border_y,x, '═')


		for y in range(1+1,bottom_border_y):
			stdscr.insstr(y,half_x, '║')
			stdscr.insstr(y,curses.COLS-1, '║')

		stdscr.insstr(1,curses.COLS-1, '╗')
		stdscr.insstr(bottom_border_y,curses.COLS-1, '╝')



def updatePanel(pad, itemList, selectedIndex, pad_height, pad_scroll_y):
	for i in range (0, min(pad_height, (len(itemList)-pad_scroll_y))):

		listIndex = pad_scroll_y + i #min(pad_scroll_y+pad_height, pad_scroll_y + (len(itemList)-pad_scroll_y))
		if i > min(pad_height, (len(itemList)-pad_scroll_y)):
			break
		
		if selectedIndex == i+pad_scroll_y:
			pad.addstr(i, 0, str(i + pad_scroll_y) + ". " + itemList[listIndex], curses.color_pair(2))
		else:
			pad.addstr(i, 0, str(i + pad_scroll_y) + ". " + itemList[listIndex])

def clamp(n, smallest, largest):
    return max(smallest, min(n, largest))


def main(stdscr):

	# Alapvető curses inicializáció
	curses.curs_set(0)  # A kurzor elrejtése
	curses.start_color()  # Színek inicializálása
	
	# Színpár létrehozása (1. színpár, fehér karakterek, kék háttér)
	curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLUE)
	curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN)

	stdscr.keypad(True)

    # Clear screen
	stdscr.clear()

	gActivePanel = 1
	half_x = int(curses.COLS/2)
	#height = curses.LINES; 
	#width = int(curses.COLS/2)
	top_border_y = 1
	bottom_border_y = curses.LINES-1-4


	#win = curses.newwin(height, width, begin_y, begin_x)
	stdscr.addstr(0, 3, 'stdscr lines: {} cols: {}'.format(curses.LINES, curses.COLS))
	draw_panel_borders(stdscr, gActivePanel)
	

	# Left Panel
	pad1 = curses.newpad(120, int(curses.COLS/2)-2)
	pad1.bkgd(' ', curses.color_pair(1))
	items1 = ["szék", "asztal", "lámpa", "toll", "könyv", "telefon", "kulcs", "autó", "láda", "kerék", "tábla", "virág", "fűnyíró", "hűtőszekrény", "teáskanna", "kés", "villa", "kanál", "szőnyeg", "pohár", "doboz", "számítógép", "laptop", "papír", "ceruza", "tükör", "szappan", "törölköző", "szék", "csésze", "fogkefe", "óra", "képernyő", "párna", "falióra", "kalapács", "fűrész", "fényképezőgép", "táska", "szemüveg", "ruhásszekrény", "bögre", "villanykörte", "naptár", "zsebkendő", "szemetes", "mappa", "lámpaernyő", "asztalterítő", "sál", "kabát", "fésű", "zokni", "sapka", "öngyújtó", "telefon", "töltő", "gitár", "hegedű", "dob", "hangszóró", "kávéfőző", "mikrohullámú sütő", "vízforraló", "porszívó", "ventilátor", "mosógép", "szárítógép", "vasaló", "lakat", "pénztárca", "kulcstartó", "szerszámosláda", "fúrógép", "csavarhúzó", "lapát", "seprű", "vödör", "távirányító", "televízió", "hifi", "kard", "köpeny", "kalap", "esernyő", "maszk", "lánc", "nyaklánc", "karóra", "fülbevaló", "gyűrű", "medál", "karkötő", "térkép", "plüssmackó", "baba", "játék", "lufi", "sakk", "kártya", "kocka", "labda", "roller (last)"]
	items1.sort()
	pad1.clear()
	pad1_selectedIndex = 0
	pad1_scroll_y = 0
	pad1_height = bottom_border_y - top_border_y - 1
	pad1_half_height = int(pad1_height / 2)
	updatePanel(pad1, items1, pad1_selectedIndex, pad1_height, pad1_scroll_y)
	
	






	
	stdscr.refresh()
	#pad1.refresh( 0,0, 0,0, 20,20)
	#stdscr.getkey()



	while True:
		#win.refresh()
		stdscr.clear()
		stdscr.addstr(0, 3, 'stdscr lines: {} cols: {}'.format(curses.LINES, curses.COLS))
		stdscr.addstr(0, 40, 'sel_index: {} scroll_y: {} panel_height: {}'.format(pad1_selectedIndex, pad1_scroll_y, pad1_height))
		draw_panel_borders(stdscr, gActivePanel)
		stdscr.refresh()

		# Panel1
		half_x = int(curses.COLS/2)
		bottom_border_y = curses.LINES-1-4
		pad1.refresh(0,0, 2,1, bottom_border_y-1,half_x-1)


		c = stdscr.getch()
		if c == ord('p'):
			#PrintDocument()
			pass
		elif c == ord('q'):
			break  # Exit the while loop
		elif c == ord('\t'):
			if gActivePanel == 1:
				gActivePanel = 2
			else:
				gActivePanel = 1
		
		elif c == curses.KEY_DOWN:
			if gActivePanel == 1:
				if pad1_selectedIndex < len(items1) -1:
					pad1.clear()
					pad1_selectedIndex = pad1_selectedIndex + 1				
					if pad1_selectedIndex - pad1_scroll_y >= pad1_height:
						pad1_scroll_y = pad1_scroll_y + pad1_half_height
						pad1_scroll_y = clamp(pad1_scroll_y, 0, len(items1)-pad1_height)
					updatePanel(pad1, items1, pad1_selectedIndex, pad1_height, pad1_scroll_y)
			elif gActivePanel == 2:
				pass

		elif c == curses.KEY_UP:
			if gActivePanel == 1:
				if pad1_selectedIndex > 0:
					pad1.clear()
					pad1_selectedIndex = pad1_selectedIndex - 1
					if pad1_selectedIndex - pad1_scroll_y < 0:
						pad1_scroll_y = pad1_scroll_y - pad1_half_height
						pad1_scroll_y = clamp(pad1_scroll_y, 0, len(items1)-pad1_height)
					updatePanel(pad1, items1, pad1_selectedIndex, pad1_height, pad1_scroll_y)
			elif gActivePanel == 2:
				pass

		elif c == curses.KEY_NPAGE: # Page Down
			if gActivePanel == 1:
				if pad1_selectedIndex < len(items1) -1:
					pad1.clear()
					pad1_selectedIndex = pad1_selectedIndex + pad1_height - 1
					pad1_selectedIndex = clamp(pad1_selectedIndex, 0, len(items1)-1)
					if pad1_selectedIndex - pad1_scroll_y >= pad1_height:
						pad1_scroll_y = pad1_scroll_y + pad1_height - 1
						pad1_scroll_y = clamp(pad1_scroll_y, 0, len(items1)-pad1_height)
					updatePanel(pad1, items1, pad1_selectedIndex, pad1_height, pad1_scroll_y)
			elif gActivePanel == 2:
				pass

		elif c == curses.KEY_PPAGE: # Page Up
			if gActivePanel == 1:
				if pad1_selectedIndex > 0:
					pad1.clear()
					pad1_selectedIndex = pad1_selectedIndex - pad1_height + 1
					pad1_selectedIndex = clamp(pad1_selectedIndex, 0, len(items1)-1)
					if pad1_selectedIndex - pad1_scroll_y < 0:
						pad1_scroll_y = pad1_scroll_y - pad1_height - 1
						pad1_scroll_y = clamp(pad1_scroll_y, 0, len(items1)-pad1_height)
					updatePanel(pad1, items1, pad1_selectedIndex, pad1_height, pad1_scroll_y)
			elif gActivePanel == 2:
				pass

		elif c == curses.KEY_END: # End
			if gActivePanel == 1:
				if pad1_selectedIndex < len(items1) -1:
					pad1.clear()
					pad1_selectedIndex = len(items1)-1
					pad1_scroll_y = len(items1)-pad1_height
					updatePanel(pad1, items1, pad1_selectedIndex, pad1_height, pad1_scroll_y)
			elif gActivePanel == 2:
				pass
		
		elif c == curses.KEY_HOME or c == 262: # Home
			if gActivePanel == 1:
				if pad1_selectedIndex > 0:
					pad1.clear()
					pad1_selectedIndex = 0
					pad1_scroll_y = 0
					updatePanel(pad1, items1, pad1_selectedIndex, pad1_height, pad1_scroll_y)
			elif gActivePanel == 2:
				pass
			
			




	curses.nocbreak()
	stdscr.keypad(False)
	curses.echo()
	curses.endwin()


if __name__ == "__main__":
    #print(__doc__)
    #print(main.__doc__)
    #input("Press enter to begin playing...")
    curses.wrapper(main)




