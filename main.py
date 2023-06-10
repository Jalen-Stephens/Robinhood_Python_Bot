import robin_stocks
from credentials import USER, PASSWORD


login = robin_stocks.robinhood.authentication.login(USER,PASSWORD)


exp_date = '2022-12-27'
#exp_date = input("The expiration date of the call option in 'YYYY-MM-DD' format.\n")
strike_call = 384.00
#strike_call = input("The strike price of the call option. EX: 399.00\n")

strike_put = 384.00
#strike_put = input("The strike price of the put option. EX: 393.00\n")
quanity = 1


limit_call = float(robin_stocks.robinhood.options.find_options_by_expiration_and_strike(inputSymbols = "SPY", expirationDate = exp_date,
    strikePrice = strike_call, optionType="call", info='mark_price')[0])

call = robin_stocks.robinhood.orders.order_buy_option_limit(positionEffect = "open", creditOrDebit = "debit", price = round(float(limit_call+.15),2),
   symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gtc', jsonify=True)
print("\n",call,"\n")
CALL  = round(float(robin_stocks.robinhood.options.find_options_by_expiration_and_strike(inputSymbols = "SPY", expirationDate = exp_date,
    strikePrice = strike_call, optionType="call", info='mark_price')[0]),2)


limit_put = round(float(robin_stocks.robinhood.options.find_options_by_expiration_and_strike(inputSymbols = "SPY", expirationDate = exp_date,
    strikePrice = strike_put, optionType="put", info='mark_price')[0]),2)

put = robin_stocks.robinhood.orders.order_buy_option_limit(positionEffect = "open", creditOrDebit = "debit", price = round(float(limit_put+.15),2),
  symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)
print("\n",put,"\n")
PUT = float(robin_stocks.robinhood.options.find_options_by_expiration_and_strike(inputSymbols = "SPY", expirationDate = exp_date,
    strikePrice = strike_put, optionType="put", info='mark_price')[0])


ask_price_call = CALL
ask_price_put = PUT

sell_point_call = round(float(CALL - (CALL*.025)),2)
sell_point_put = round(float(PUT - (PUT*.025)),2)
sell_point_high_call = round(float(CALL - (CALL*.015)),2)
sell_point_high_put = round(float(PUT - (PUT*.015)),2)


prof_target_Call = round(float(CALL + (CALL*.05)),2)
prof_target_Put = round(float(PUT + (PUT*.05)),2)
prof_low_Call = round(float(CALL + (CALL*.0125)),2)
prof_low_Put = round(float(PUT + (PUT*.0125)),2)
print("\n\nInitial Call Price:",CALL)
print("Sell point Call: ",sell_point_call)
print("Profit target Call: ",prof_target_Call)
print("Profit low target Call: ",prof_low_Call)
print("\nInitial Put Price:",PUT)
print("Sell point Put: ",sell_point_put)
print("Profit target Put: ", prof_target_Put)
print("Profit low target Put: ",prof_low_Put)


def refresh_call():
    return round(float(robin_stocks.robinhood.options.find_options_by_expiration_and_strike(inputSymbols = "SPY", expirationDate = exp_date,
                    strikePrice = strike_call, optionType="call", info='mark_price')[0]),2)


def refresh_put():
    return round(float(robin_stocks.robinhood.options.find_options_by_expiration_and_strike(inputSymbols = "SPY", expirationDate = exp_date,
                    strikePrice = strike_put, optionType="put", info='mark_price')[0]),2)


def monitor_call(put_percentage, check):

    print("Sell Point Call: ", prof_low_Call)
    run=0
    if check == 1:

        while run>=0:

            curr_mon_call = refresh_call()
            print("Current price: ",curr_mon_call,"\t",round(float(-1*(((CALL/curr_mon_call)*100)-100)),2),"\n")
            run+=1

            if curr_mon_call<=prof_low_Call:

                call = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(prof_low_Call-.15),2)
                            ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gfd', jsonify=True)
        
                print("\n",call,"\n")
                x = refresh_call()
                print("SOLD @ ", x)
                print("\nTotal Profit: ",round((put_percentage) + (((x-CALL)/CALL)*100),2),"%")
                break
            elif curr_mon_call>=prof_target_Call:

                call = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(prof_low_Call),2)
                            ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gfd', jsonify=True)
        
                print("\n",call,"\n")
                x = refresh_call()
                print("SOLD @ ", x)
                print("\nTotal Profit: ",round((put_percentage) + (((x-CALL)/CALL)*100),2),"%")
                break
    else:

        while run>=0:

            curr_mon_call = refresh_call()
            print("Current price: ",curr_mon_call,"\t",round(float(-1*(((CALL/curr_mon_call)*100)-100)),2),"\n")
            run+=1

            if curr_mon_call<=sell_point_call:

                call = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(sell_point_call-.1),2)
                            ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gfd', jsonify=True)
        
                print("\n",call,"\n")
                x = refresh_call()
                print("SOLD @ ", x)
                print("\nTotal Profit: ",round((put_percentage) + (((x-CALL)/CALL)*100),2),"%")
                break
            elif curr_mon_call>= sell_point_high_call:

                call = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(sell_point_high_call-.1,2)
                            ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gfd', jsonify=True)
        
                print("\n",call,"\n")
                x = refresh_call()
                print("SOLD @ ", x)
                print("\nTotal Profit: ",round((put_percentage) + (((x-CALL)/CALL)*100),2),"%")
                break

    


def monitor_put(call_percentage, check):

    print("Sell Point Put: ", prof_low_Put)
    run = 0
    if check == 1:

        while run>=0:

            curr_mon_put = refresh_put()
            print("Current price: ",curr_mon_put,"\t",round(float(-1*(((PUT/curr_mon_put)*100)-100)),2),"\n")
            run+=1

            if curr_mon_put <= prof_low_Put:

                put = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(sell_point_put-.1),2)
                         ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)

                print("\n",put,'\n')
                x = refresh_put()
                print("SOLD @ ", x)
            
                print("\nTotal Profit: ",round((call_percentage) + (((x-PUT)/PUT)*100),2),"%")
                break
            elif curr_mon_put >= prof_target_Put:

                put = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(prof_low_Put),2)
                         ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)

                print("\n",put,'\n')
                x = refresh_put()
                print("SOLD @ ", x)
            
                print("\nTotal Profit: ",round((call_percentage) + (((x-PUT)/PUT)*100),2),"%")
                break
    else:

        while run>=0:

            curr_mon_put = refresh_put()
            print("Current price: ",curr_mon_put,"\t",round(float(-1*(((PUT/curr_mon_put)*100)-100)),2),"\n")
            run+=1

            if curr_mon_put <= sell_point_put:

                put = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(sell_point_put-.1),2)
                         ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)

                print("\n",put,'\n')
                x = refresh_put()
                print("SOLD @ ", x)
            
                print("\nTotal Profit: ",round((call_percentage) + (((x-PUT)/PUT)*100),2),"%")
                break
            elif curr_mon_put >= sell_point_high_put:

                put = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(sell_point_high_put-.1,2)
                         ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)

                print("\n",put,'\n')
                x = refresh_put()
                print("SOLD @ ", x)
            
                print("\nTotal Profit: ",round((call_percentage) + (((x-PUT)/PUT)*100),2),"%")
                break



def sell(key,check):

    
    if key == 0:
        if check == 1:

            put = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(sell_point_put-.1),2)
                         ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)
        else:
            put = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(prof_low_Put),2)
                         ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)

        print("\n",put,'\n')
        x = refresh_put()
        print("Put was sold at : ",x,"\n")
        
        print("\n" + ("*"*5)+ "\tMonitoring Call Option\t" + ("*"*5) +"\n" )
        
        monitor_call(float(((x-PUT)/PUT)*100), check)
    elif key == 1:

        if check ==1:

            call = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(sell_point_call-.1),2)
                            ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gfd', jsonify=True)
        else:
            call = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(prof_low_Call),2)
                         ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gfd', jsonify=True)

                         
        print("\n",call,'\n')
        x = refresh_call()
        print("Call was sold at : ", x,"\n")
        
        print("\n " + ("*"*5)+ "\tMonitoring Put Option\t" + ("*"*5) )
        
        monitor_put(float(((x-CALL)/CALL)*100), check)


count = 0
while count>=0:
    

    curr_call,curr_put = refresh_call(),refresh_put()

    if count==0:
        print("\nCall Price\t\t\tCall %\t\t\tPut Price\t\tPut % \n")
    else:
        print(curr_call,"\t\t\t\t",round(float(-1*(((CALL/curr_call)*100)-100)),2),"\t\t\t",curr_put,"\t\t\t",round(float(-1*(((PUT/curr_put)*100)-100)),2),"\n")
    count+=1


    if curr_call >= prof_target_Call:
        sell(1,0)
        break
    elif curr_put >= prof_target_Put:
        sell(0,0)
        break
    elif curr_call<=sell_point_call:
        sell(0,1)
        break
    elif curr_put<=sell_point_put:
        sell(1,1)
        break


print("All done\n")