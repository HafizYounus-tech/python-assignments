import streamlit as st
import pandas as pd
import random 
import plotly.express as px
from datetime import datetime

try:
    all_accounts = pd.read_csv("bank_accounts.csv")
except pd.errors.EmptyDataError:
    all_accounts = pd.DataFrame()


try:
    traction_history = pd.read_csv("transaction_history.csv")
except pd.errors.EmptyDataError:
    traction_history = pd.DataFrame()

def safe_password():
    while True:
        password = random.randint(1000, 9999)
        duplicate = False

        for index, row in all_accounts.iterrows():
            if row["password"] == password:
                duplicate = True
                break

        if duplicate == False:
            break
    return password

def safe_account_number():
    while True:
        acc_num = random.randint(10000,99999)
        duplicate = False

        for index,row in all_accounts.iterrows():
            if row["account_number"] == acc_num:
                duplicate = True
                break

        if duplicate == False:
            break
    return acc_num

def duplicate_cnic(cnic):
    try:
        for index,row in all_accounts.iterrows():
            if row["cnic"] == int(cnic):
                st.error("This CNIC is already registered with our bank.")
                st.warning("Please enter a different, valid CNIC number.")
                break
        else:
            return  cnic
    except ValueError:
        st.error('please enter valid cnic')

def open_account(tittle,cnic,contact_num,balance=0):
    global all_accounts
    global traction_history

    if((tittle.replace(" ","")).isalpha()):
        cnic_num = duplicate_cnic(cnic)
        if cnic_num is not None:
            if len(cnic_num) == 13 and cnic_num.isdigit():
                if len(contact_num) == 11 and contact_num.isdigit():
                    if not(balance < 0):
                        password = safe_password()
                        account_num = safe_account_number()
                        account  = {
                            "tittle" : [tittle],
                            "cnic" : [cnic_num],
                            "contact_number" : [contact_num],
                            "password" : [password],
                            "balance" : [balance],
                            "account_number": [account_num]
                        }
                        new_acc = pd.DataFrame(account)
                        all_accounts = pd.concat([all_accounts,new_acc],ignore_index=True)
                        all_accounts.to_csv("bank_accounts.csv",index=False)
                        transaction = {
                            "date_and_time" : [datetime.now()],
                            "title" : [tittle],
                            "account_number" : [account_num],
                            "password" : [password],
                            "type" : ["initial deposit"],
                            "amount" : [balance]     
                        }
                        new_transaction = pd.DataFrame(transaction)
                        traction_history = pd.concat([traction_history,new_transaction],ignore_index=True)
                        traction_history.to_csv("transaction_history.csv",index=False)
                        return new_acc
                    else:
                        st.error("please enter valid amount")
                else:
                    st.error("contact number must be 11 digit , without deches")
            else:
                st.error(f"cnic must be 13 digit , without deches ")
    else:
        st.error(" Please enter a valid name (letters only).")

def check_balance(account_number,password):
    for _,row in all_accounts.iterrows():
        if account_number == row["account_number"]:
            if password == row["password"]:
                return row
            else:
                st.error("**❌ Incorrect password. please try again**")
            break
    else:
        st.error("**❌ No account found with this account number.**.")

def withrwa(account_num, password,amount):
    global traction_history
    for _,acc in all_accounts.iterrows():
        if account_num == acc["account_number"]:
            if password == acc["password"]:
                if amount > 0:
                    if acc["balance"] >= amount:
                        all_accounts.loc[all_accounts["account_number"] == account_num, "balance"] -= amount
                        all_accounts.to_csv("bank_accounts.csv", index=False)
                        transaction = {
                            "date_and_time" : [datetime.now()],
                            "title" : [acc["tittle"]],
                            "account_number" : [account_num],
                            "password" : [password],
                            "type" : ["withdraw"],
                            "amount" : [amount]     
                        }
                        new_transaction = pd.DataFrame(transaction)
                        traction_history = pd.concat([traction_history,new_transaction],ignore_index=True)
                        traction_history.to_csv("transaction_history.csv",index=False)
                        st.success(f"✅ Rs.**{amount}** withdrawal successfully. Current balance:**{all_accounts.loc[all_accounts["account_number"] == account_num, "balance"].iloc[0]}**")
                        break
                    else:
                        st.error(f"**❌ Insufficient balance.**")
                        break
                else:
                    st.error( f"**❌ Amount must be greater than 0.**")
                    break
            else:
                st.error( f"**❌ Incorrect password.**")
                break
    else:
        st.error(f"**❌ Account number not found**.")

def deposite(account_num, password, amount):
    global traction_history
    for _,acc in all_accounts.iterrows():
        if account_num == acc["account_number"]:
            if password == acc["password"]:
                if amount > 0:
                    all_accounts.loc[all_accounts["account_number"] == account_num, "balance"] += amount
                    all_accounts.to_csv("bank_accounts.csv", index=False)
                    st.success(f"✅ Rs.**{amount}** deposited successfully. Current balance:**{all_accounts.loc[all_accounts["account_number"] == account_num, "balance"].iloc[0]}**")
                    transaction = {
                        "date_and_time" : [datetime.now()],
                        "title" : [acc["tittle"]],
                        "account_number" : [account_num],
                        "password" : [password],
                        "type" : ["deposit"],
                        "amount" : [amount]     
                    }
                    new_transaction = pd.DataFrame(transaction)
                    traction_history = pd.concat([traction_history,new_transaction],ignore_index=True)
                    traction_history.to_csv("transaction_history.csv",index=False)
                    break
                else:
                    st.error( f"**❌ Amount must be greater than 0.**")
                    break
            else:
                st.error( f"**❌ Incorrect password.**")
                break
    else:
        st.error( f"**❌ Account number not found**.")

def transfer( acc_num, password,transfer_amount,transfer_acc):
    global traction_history
    for _,acc in all_accounts.iterrows():
        if acc_num == acc["account_number"]:
            if password == acc["password"]:
                if transfer_amount > 0:
                    if acc["balance"] >= transfer_amount:
                        for _,trans_acc in all_accounts.iterrows():
                            if trans_acc["account_number"] == transfer_acc:
                                all_accounts.loc[all_accounts["account_number"] == acc_num , "balance"] -= transfer_amount
                                all_accounts.loc[all_accounts["account_number"] == transfer_acc , "balance"] += transfer_amount
                                all_accounts.to_csv("bank_accounts.csv",index= False)
                                transaction = {
                                    "date_and_time" : [datetime.now()],
                                    "title" : [acc["tittle"]],
                                    "account_number" : [acc_num],
                                    "password" : [password],
                                    "type" : ["transfer_sent"],
                                    "amount" : [transfer_amount],
                                    "Recipent_account" : [transfer_acc]   
                                }
                                reciver = {
                                    "date_and_time" : [datetime.now()],
                                    "type" : ["transfer_received"],
                                    "amount" : [transfer_amount],
                                    "Recipent_account" : [acc_num]
                                }
                                df_reciver = pd.DataFrame(reciver)
                                traction_history = pd.concat([traction_history,df_reciver],ignore_index=True)
                                traction_history.to_csv("transaction_history.csv",index=False)
                                new_transaction = pd.DataFrame(transaction)
                                traction_history = pd.concat([traction_history,new_transaction],ignore_index=True)
                                traction_history.to_csv("transaction_history.csv",index=False)
                                st.success( f"Transfer of Rs.**{transfer_amount}** was successful to account **{transfer_acc}** ")
                                break 
                        else:
                            st.error( f"❌ Recipient account not found.")
                            break
                    else:
                        st.error( f"**❌ Incificent balance: **")
                        break
                else:   
                    st.error( f"**❌ Amount must be greater than 0.**")
                    break
            else:
                st.error( f"**❌ Incorrect password.**")
                break
            break
    else:
        st.error( f"**❌ Account number not found**.")

def close_account(acc_num, password):
    for index,acc in all_accounts.iterrows():
        if acc["account_number"] == acc_num:
            if acc["password"] == password:
                st.success(f"Your final balance of Rs. {acc['balance']} has been returned.")
                all_accounts.drop(index=index,inplace=True)
                all_accounts.to_csv("bank_accounts.csv",index=False)
                st.success("Your account has been permanently closed.")
                break
            else:
                st.error("Incorrect password. Please try again.")
                break
    else:
        st.error("No account found with this account number.")

def trans_history(acc_num,pin):
    all_transaction = []
    for _,acc in traction_history.iterrows():
        if acc["account_number"] == acc_num:
            if acc["password"] == pin:
                all_transaction.append(acc)                
            else:
                st.error("incorrect password")
                break
    df_transaction = pd.DataFrame(all_transaction)
    return df_transaction


st.set_page_config("First Project",layout="wide",page_icon="🏦")
st.title('🏦 SecureBank | Banking Redefined')
st.caption('Hafiz Banking Systems')
st.divider()
st.title("Bank Management System", text_alignment="center")
st.caption("Created by Hafiz Younus",text_alignment="center")

if "page" not in st.session_state:
    st.session_state.page = "home"

if  st.session_state.page == "home":
    st.subheader("What would you like to do?", text_alignment="center")
    st.caption('Select an option below to perform account operations quickly and securely.', text_alignment="center")
    st.divider()
    first,second=st.columns(2)
    third,four = st.columns(2)
    five,six = st.columns(2)

    first = first.button("OPEN ACCOUNT",width="stretch",type="secondary",icon="🆕")
    second = second.button("TRANSFER MONEY",width="stretch",type="secondary",icon="🔄")
    third = third.button("CHECK BALANCE",width="stretch",type="secondary",icon="💳")
    forth = four.button("WITHDRAW MONEY",width="stretch",type="secondary",icon="💸")
    fiveth = five.button("DEPOSIT MONEY",width="stretch",type="secondary",icon="📥")
    sixth = six.button("CLOSE ACCOUNT",width="stretch",type="primary",icon="🔒")
    seven = st.button("TRANSACTION HISTORY",width="stretch",icon='📊')

    st.divider()

    if first:
        st.session_state.page = "open_account"
        st.rerun()

    elif second:
        st.session_state.page = "transfer amount"
        st.rerun()

    elif third:
        st.session_state.page = "check_balance"
        st.rerun()

    elif forth:
        st.session_state.page = "withdraw"
        st.rerun()

    elif fiveth:
        st.session_state.page = "deposit"
        st.rerun()

    elif sixth:
        st.session_state.page = "close account"
        st.rerun()

    elif seven:
        st.session_state.page = "transaction history"
        st.rerun()
    

def back_home():
    if st.button("🔙 BACK TO HOME",type="primary"):
        st.session_state.page = "home"
        st.rerun()

if st.session_state.page == "open_account":
    st.subheader("🆕OPEN ACCPOUNT",text_alignment="center")
    with st.form("open account"):
        try:
            tittle = st.text_input("Enter your account tittle: ")
        except ValueError:
            st.error("please enter valid name")
        cnic = st.text_input("Enter your cnic number without deshes(-): ",placeholder="4220XXXXXXXXX",max_chars=13)
        balance = st.number_input("Enter your initial deposite: ",step=1,value=None)
        if balance is None:
            balance = 0
        contact_number = st.text_input("Enter your contact number: ", placeholder="03XXXXXXXXX",max_chars=11)
        button = st.form_submit_button()
        if button:
            if tittle and contact_number and cnic:
                result = open_account(tittle,cnic,contact_number,balance)
                if result is not None:
                    st.session_state.result = result
                    st.session_state.page = "opened_account"
                    st.rerun()
            else:
                st.error("please fill the form information")
    back_home()

if st.session_state.page == "opened_account":
    st.subheader("ACCOUNT OPENED",icon="🎉")
    st.success("YOUR ACCOUNT SUCCESSFULLY CREATED")
    st.divider()
    col1,col2,col3 = st.columns(3)
    with col1:
        st.metric("YOUR ACCOUNT NUMBER",value= st.session_state.result["account_number"].iloc[0],border=True)
    with col2:
        st.metric("YOUR ACCOUNT PASSWORD",value= st.session_state.result["password"].iloc[0],border=True)
    with col3:
        st.metric("YOUR ACCOUNT BALANCE",value= st.session_state.result["balance"].iloc[0],border=True)
    st.divider()

    st.warning(f"⚠️ Don't forget: Account Number **{st.session_state.result["account_number"].iloc[0]}** and Password **{st.session_state.result["password"].iloc[0]}**")
    st.balloons()
    back_home()

if st.session_state.page == "check_balance":
    st.subheader("💳CHECK BALANCE",text_alignment="center")
    with st.form("check balance"):
        acc_num = st.text_input("Enter your account number: ").strip()
        pin = st.text_input("Enter your account password: ",type="password").strip()
        if st.form_submit_button():
            if acc_num and pin:
                try:
                    acc = check_balance(int(acc_num),int(pin))
                    if  acc is not None:
                        col1,col2,col3 = st.columns(3)
                        with col1:
                            st.metric("**this is your account number:**", value=acc["account_number"],border=True)
                        with col2:
                            st.metric("**this is your password number:**", value=acc["password"],border=True)
                        with col3:
                            st.metric("**this is your balance:**", value=acc["balance"],border=True)
                except ValueError:
                    st.error("please enter valid details")
                
            else:
                st.error("please fill the form information")
            
    back_home()
    

if st.session_state.page == "withdraw":
    st.subheader("💸WITHDRAW",text_alignment="center")
    with st.form("withdraw"):
        acc_num = st.text_input("**Enter your account number**").strip()
        pin = st.text_input("**Enter your account password**",type="password").strip()
        try:
            amount = st.number_input("**Enter withdraw amount**",value=None,step=1)
            if st.form_submit_button():
                if acc_num and pin :
                    try:
                        withrwa(int(acc_num),int(pin),amount)
                    except ValueError:
                        st.error("please enter valid details")

                else:
                    st.error("**Please fill the form information** ")
        except TypeError:
            st.error('Please enter amount')
                
    back_home()

if st.session_state.page == "deposit":
    st.subheader("📥DEPOSIT",text_alignment="center")
    with st.form("deposit"):
        acc_num = st.text_input("**Enter your account number**").strip()
        pin = st.text_input("**Enter your account password**",type="password").strip()
        try:
            amount = st.number_input("**Enter deposit amount**",value=None,step=1)
            if st.form_submit_button():
                if acc_num and pin:
                    try:
                        deposite(int(acc_num),int(pin),amount)
                    except ValueError:
                        st.error("please enter valid details")
    
                else:
                    st.error("**Please fill the form information** ")
        except TypeError:
            st.error('Please enter amount')

    back_home()

if st.session_state.page == "transfer amount":
    st.subheader("🔄TRANSFER AMOUNT",text_alignment="center")
    with st.form("transfer amount"):
        acc_num = st.text_input("Enter account number for transfer amount:").strip()
        pin = st.text_input("Enter account password for transfer amount:",type="password").strip()
        amount = st.number_input("Enter amount to transfer:",value=None,step=1)
        transfer_acc = st.text_input("Enter recipient account number:").strip()
        if st.form_submit_button():
            if acc_num and pin and transfer_acc :
                try:
                    transfer(int(acc_num),int(pin),amount,int(transfer_acc))
                except ValueError:
                    st.error("please enter valid details")
            else:
                st.error("please fill the form information")
    back_home()

if st.session_state.page == "close account":    
    st.subheader("🔒 close account",text_alignment="center")
    with st.form("close account"):
        acc_num = st.text_input("Enter account number for close account:").strip()
        pin = st.text_input("Enter account password for close account:",type="password").strip()
        if st.form_submit_button():
            if acc_num and pin:
                try:
                    close_account(int(acc_num),int(pin))
                except ValueError:
                    st.error("please enter valid details")
                
            else:
                st.error("please fill form information")
    back_home()
   
if st.session_state.page == "transaction history":
    st.subheader("transction history",text_alignment="center")
    with st.form("transction history"):
        acc_num = st.text_input("Enter account number:").strip()
        pin = st.text_input("Enter account password :",type="password").strip()
        if st.form_submit_button():
            if acc_num and pin:
                try:
                    transaction = trans_history(int(acc_num),int(pin))
                except ValueError:
                    st.error("please enter valid details")
                if transaction.empty:
                    st.warning("abhi tak koi transaction nhi ki ha apny")
                else:
                    st.session_state.history = transaction
                    st.session_state.page = "self_transaction_history"
                    st.rerun()
            else:
                st.error("please fill the form")

    back_home()

if st.session_state.page == "self_transaction_history":
    st.subheader("Transaction History",text_alignment="center")
    transactions = st.session_state.history
    col1 , col2 = st.columns(2)
    col3 , col4 = st.columns(2)
    col5 , col6 = st.columns(2)
    total = transactions["amount"].sum()
    total_withdraws = transactions[transactions["type"] == "withdraw"]["amount"].sum()
    total_deposit = transactions[transactions["type"] == "deposit"]["amount"].sum()
    total_recive = transactions[transactions["type"] == "transfer_received"]["amount"].sum()
    initial_deposite = transactions[transactions["type"] == "initial deposit"]["amount"].sum()
    total_sent = transactions[transactions["type"] == "transfer_sent"]["amount"].sum()
    with col1:
        st.metric('Total Transactions Amount',f"PKR:{total}", border=True)
    with col2:
        st.metric("Total Withdrawals",f"PKR:{total_withdraws}",border=True)
    with col3:
        st.metric("Total Deposits",f"PKR:{total_deposit}",border=True)
    with col4:
        st.metric("Total Amount Received",f"PKR:{total_recive}",border=True)
    with col5:
        st.metric("Initial Deposit",f"PKR:{initial_deposite}",border=True)
    with col6:
        st.metric("Total Amount Sent",f"PKR:{total_sent}",border=True)

    labels = ['Initial Deposit', 'Total Sent', 'Total Received', 'Total Deposits', 'Total Withdrawals']
    values = [initial_deposite, total_sent, total_recive, total_deposit, total_withdraws]
    fig_pie = px.pie(names=labels, values=values, title='Transactions Breakdown')
    fig_bar = px.bar(x=labels,y=values,labels={'x': 'Transaction Type', 'y': 'Amount (PKR)'},title='Transactions Bar Chart')
    c1,c2 = st.columns(2)
    with c1:
        st.plotly_chart(fig_pie)
    with c2:
        st.plotly_chart(fig_bar)

    back_home()