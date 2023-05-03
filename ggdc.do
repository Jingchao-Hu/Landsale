clear

*root directory:
local root ="C:/Users/macbook/Desktop/RA/emp data"
*output file:
local output="`root'/result data/newggdc.dta"
*raw data:
use "`root'/original data/ggdc.dta"

keep if Variable=="EMP"


drop Variable Region Regioncode SUM
rename AGR Agriculture
rename MIN Mining
rename MAN Manufacturing
rename PU Utilities
rename CON Construction
rename WRT Trade
rename TRA Transport
rename FIRE Business
rename GOV Government
rename OTH Others


gather Agriculture Mining Manufacturing Utilities Construction Trade Transport Business Government Others, variable(industry)

drop if value==.

gen country_code=Country

order Country country_code Year industry value

rename Country country
rename country_code geo_code
rename Year year



save "`output'",replace