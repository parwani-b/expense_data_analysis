# expense_data_analysis
This repository contains my latest work for exploratory data analysis of my everyday expenses. Below is the explanation of how to use this tool for expense analysis -

-------------------------------------    How does expense_data_dump script functions? -------------------------------------

1] The expense_data_dump.py script takes the expense data in csv format and drops any unnecessary columns in the data that are not needed for exploratory analysis like names of people, currency. We can also drop any other columns from the data that are irrelevant for the analysis

2] It assigns unique IDs to each expense data row

3] TRUNCATES the already existing data in MySQL table so that it can add fresh data during every script run so that we get updated data every time (think of a case when I ordered a product from Amazon and entered it in my expense data but returned that product a week later because I realized I don't need it and so deleted this expense from my expense data)

4] Stores fresh data from the csv file to MySQL table

------------------------------------    How does expense_tracker_menu script functions? ------------------------------------

1] The initial run of the script provides the user with 3 options:
   
    i.    Track expenses for current year
   
    ii.   Track expenses for last year
   
    iii.  Track expenses for the year of your choice

2] Once the user inputs their choice, it provides the user with 11 options:
   
    i.    How much total monthly expense I had in a specific month?
   
    ii.   How much dining out expenses I had in a specific month?
   
    iii.  How much grocery expenses I had in a specific month?
   
    iv.   How much gas/fuel expenses I had in a specific month?
   
    v.    How much household supplies expenses I had in a specific month?
  
    vi.   How much car expenses I had in a specific month?
   
    vii.  How much hotel expenses I had in a specific month?
   
    viii. How much heat/gas expenses I had in a specific month?
   
    ix.   How much electricity expenses I had in a specific month?
   
    x.    What is the most highest expense I had (other than rent) in a specific month?
   
    xi.   What is my average monthly expense for a specific year?

3] Once the user inputs their choice, it asks the user to enter the month of that year for which they would like to track their expense

4] After the user provides the choice of their month and hit enter, the script queries the back-end MySQL table based on the user inputs and provides the expense output/result to the user for any category of their choice. 

5] This tool can help the user to track/review their expenses and undersand where they stand with their expenses at a specific time of the month/year and can also provide the running average of their expenses at any any point during the year and helps them make informed decisions. It also gives them insights and a chance to make any changes to their budget/spendings for any specific category if they want.  

   

