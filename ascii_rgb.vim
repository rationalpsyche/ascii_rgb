" Vim global plugin to save a map color:characters selection
" Last Change: 2022 February 2
" Maintainer: Nicolò Fornari

function! SaveCursorWithColor(color)
	let ascii_rgb = "./ascii_rgb.py"
	" get file name
	:normal :f
	let ascii_file = @%
	let color_file = ascii_file . ".colors"

	let [line_start, column_start] = getpos("'<")[1:2]
	let [line_end, column_end] = getpos("'>")[1:2]
	let color_and_position = a:color.",".line_start.",".column_start.",".line_end.",".column_end
	let line = [color_and_position]

	:silent execute "!touch " . color_file
	":redraw!
	:call writefile(line, color_file,"a")
	:silent execute "!python3 " . ascii_rgb . " --ascii " . ascii_file . " --colors " . color_file
	:redraw!

endfunction

function! Reset()
	" get file name
	:normal :f
	let ascii_file = @%
	let color_file = ascii_file . ".colors"

	:execute "!rm " . color_file
	:redraw!
endfunction

" module is intended on a line basis
" if multiple lines are selected then <c-u> prevents the range to be added causing multiple
" function calls for each selected line

nnoremap <leader>res :call Reset()<cr>
nnoremap <leader>tt :<c-u>call SaveCursorWithColor("COLOR_NC")<cr>
vnoremap <leader>red :<c-u>call SaveCursorWithColor("RED")<cr>
vnoremap <leader>gre :<c-u>call SaveCursorWithColor("GREEN")<cr>
vnoremap <leader>gra :<c-u>call SaveCursorWithColor("GRAY")<cr>
vnoremap <leader>cya :<c-u>call SaveCursorWithColor("CYAN")<cr>
vnoremap <leader>yel :<c-u>call SaveCursorWithColor("YELLOW")<cr>
vnoremap <leader>blu :<c-u>call SaveCursorWithColor("BLUE")<cr>
vnoremap <leader>pur :<c-u>call SaveCursorWithColor("PURPLE")<cr>
vnoremap <leader>whi :<c-u>call SaveCursorWithColor("WHITE")<cr>
vnoremap <leader>bro :<c-u>call SaveCursorWithColor("BROWN")<cr>
vnoremap <leader>lgre :<c-u>call SaveCursorWithColor("LIGHT_GREEN")<cr>
vnoremap <leader>lred :<c-u>call SaveCursorWithColor("LIGHT_RED")<cr>
vnoremap <leader>lgre :<c-u>call SaveCursorWithColor("LIGHT_GREEN")<cr>
vnoremap <leader>lgra :<c-u>call SaveCursorWithColor("LIGHT_GRAY")<cr>
vnoremap <leader>lcya :<c-u>call SaveCursorWithColor("LIGHT_CYAN")<cr>
vnoremap <leader>lblu :<c-u>call SaveCursorWithColor("LIGHT_BLUE")<cr>
vnoremap <leader>lpur :<c-u>call SaveCursorWithColor("LIGHT_PURPLE")<cr>
vnoremap <leader>gre :<c-u>call SaveCursorWithColor("GREEN")<cr>
