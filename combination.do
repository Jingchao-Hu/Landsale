clear

use "C:/Users/macbook/Desktop/RA/emp data/result data/newggdc.dta"

append using "C:/Users/macbook/Desktop/RA/emp data/result data/neweuklems.dta"

append using "C:/Users/macbook/Desktop/RA/emp data/result data/newoecd.dta"
save "C:/Users/macbook/Desktop/RA/emp data/result data/combination.dta" ,replace
