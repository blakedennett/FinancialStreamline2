

import shutil
from datetime import datetime


# ====================================================================================================================================================================================
# Dates
# ====================================================================================================================================================================================


now = datetime.now()
year = now.year
month = now.month

# Move back one month
if month == 1:
    month = 12
    year -= 1
else:
    month -= 1

last_month = datetime(year, month, 1).strftime("%b")
current_yr = datetime.now().year % 100


# ====================================================================================================================================================================================
# Archive credit history 
# ====================================================================================================================================================================================


source_path = r"C:\Users\Denne\Documents\VSCodeProjects\FinancialStreamline2\BankStreamline\Data\CreditHistory.csv"
destination_path = fr"C:\Users\Denne\Documents\VSCodeProjects\FinancialStreamline2\BankStreamline\Data\dataArchives\creditArchive\CreditHistory_{last_month}{current_yr}.csv"

# shutil.move(source_path, destination_path)



# ====================================================================================================================================================================================
# Archive dedit history 
# ====================================================================================================================================================================================


source_path = r"C:\Users\Denne\Documents\VSCodeProjects\FinancialStreamline2\BankStreamline\Data\DebitHistory.csv"
destination_path = fr"C:\Users\Denne\Documents\VSCodeProjects\FinancialStreamline2\BankStreamline\Data\dataArchives\debitArchive\CreditHistory_{last_month}{current_yr}.csv"

# shutil.move(source_path, destination_path)



# ====================================================================================================================================================================================
# Move/rename new debit file
# ====================================================================================================================================================================================


source_path = r"C:\Users\Denne\Downloads\AccountHistory.csv"
destination_path = fr"C:\Users\Denne\Documents\VSCodeProjects\FinancialStreamline2\BankStreamline\Data\DebitHistory.csv"

# shutil.move(source_path, destination_path)




# ====================================================================================================================================================================================
# Move/rename new credit file
# ====================================================================================================================================================================================


source_path = r"C:\Users\Denne\Downloads\download.csv"
destination_path = fr"C:\Users\Denne\Documents\VSCodeProjects\FinancialStreamline2\BankStreamline\Data\CreditHistory.csv"

# shutil.move(source_path, destination_path)

