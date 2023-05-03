*** Import Data
insheet using "C:/Users/macbook/Desktop/RA/emp data/original data/OECD.csv", clear

*** Extract Data
replace industry = substr(industry, strpos(industry, "[") + 1, ///
strpos(industry, "]") - strpos(industry, "[") - 1) 


bysort country time: egen H = sum(value * (industry == "H"))
bysort country time: egen J = sum(value * (industry == "J"))
bysort country time: egen L_N = sum(value * (industry == "L-N"))

bysort country time: replace value = value - H if industry == "G-I"
bysort country time: replace value = value + J if industry == "H"
bysort country time: replace value = value + L_N if industry == "K"

keep if industry == "A"|industry == "B"| industry == "C"| industry == "D-E"| ///
industry == "F"| industry == "G-I"| industry == "H"| industry == "K"| ///
industry == "O-Q" |industry == "R-U"

replace industry = "Agriculture" if industry == "A"
replace industry = "Mining" if industry == "B"
replace industry = "Manufacturing" if industry == "C"
replace industry = "Utilities" if industry == "D-E"
replace industry = "Construction" if industry == "F"
replace industry = "Trade" if industry == "G-I"
replace industry = "Transport" if industry == "H"
replace industry = "Business" if industry == "K"
replace industry = "Government" if industry == "O-Q"
replace industry = "Others" if industry == "R-U"

rename location geo_code
rename time year

keep country geo_code year industry value
order country geo_code year industry value
*** Export data


drop if missing(value)

save "C:\Users\macbook\Desktop\RA\emp data\result data\newoecd.dta",replace


