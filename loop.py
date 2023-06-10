import robin_stocks
import time
from credentials import USER, PASSWORD


login = robin_stocks.robinhood.authentication.login(USER,PASSWORD)


exp_date = '2022-12-27'

strike_call = 384.00

strike_put = 384.00

quanity = 1
i =0

total_prof = []
while i<1:

    

    if( sum(total_prof) <= -10.00):
        print("Sum is :", sum(total_prof))
        print("program ending")
        break

    #time.sleep(5)

    limit_call = float(robin_stocks.robinhood.options.find_options_by_expiration_and_strike(inputSymbols = "SPY", expirationDate = exp_date,
        strikePrice = strike_call, optionType="call", info='mark_price')[0])
    
    call = robin_stocks.robinhood.orders.order_buy_option_limit(positionEffect = "open", creditOrDebit = "debit", price = round(float(limit_call+.2),2),
        symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gtc', jsonify=True)
    
    CALL  = float(robin_stocks.robinhood.options.find_options_by_expiration_and_strike(inputSymbols = "SPY", expirationDate = exp_date,
        strikePrice = strike_call, optionType="call", info='mark_price')[0])


    limit_put = float(robin_stocks.robinhood.options.find_options_by_expiration_and_strike(inputSymbols = "SPY", expirationDate = exp_date,
        strikePrice = strike_put, optionType="put", info='mark_price')[0])

    put = robin_stocks.robinhood.orders.order_buy_option_limit(positionEffect = "open", creditOrDebit = "debit", price = round(float(limit_put+.2),2),
        symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)
    
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
    


    def refresh_call():
        return round(float(robin_stocks.robinhood.options.find_options_by_expiration_and_strike(inputSymbols = "SPY", expirationDate = exp_date,
                        strikePrice = strike_call, optionType="call", info='mark_price')[0]),2)


    def refresh_put():
        return round(float(robin_stocks.robinhood.options.find_options_by_expiration_and_strike(inputSymbols = "SPY", expirationDate = exp_date,
                        strikePrice = strike_put, optionType="put", info='mark_price')[0]),2)


    def monitor_call(put_percentage, check):

        run=0
        if check == 1:

            while run>=0:

                run+=1
                curr_call = refresh_call()
                if curr_call<=prof_low_Call:

                    call = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(prof_low_Call-.2),2)
                            ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gfd', jsonify=True)

                    x = refresh_call()
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(round((put_percentage) + (((x-CALL)/CALL)*100),2),"\t\t",current_time)
                    total_prof.append(round((put_percentage) + (((x-CALL)/CALL)*100),2))

                    break
                elif curr_call>=prof_target_Call:
                    
                    call = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(prof_low_Call),2)
                            ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gfd', jsonify=True)
        

                    x = refresh_call()
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(round((put_percentage) + (((x-CALL)/CALL)*100),2),"\t\t",current_time)
                    total_prof.append(round((put_percentage) + (((x-CALL)/CALL)*100),2))
                    break
        else:

            while run>=0:
                run+=1
                curr_call = refresh_call()
                if curr_call<=sell_point_call:

                    call = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(sell_point_call-.2),2)
                            ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gfd', jsonify=True)
        
                    
                    x = refresh_call()
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(round((put_percentage) + (((x-CALL)/CALL)*100),2),"\t\t",current_time)
                    total_prof.append(round((put_percentage) + (((x-CALL)/CALL)*100),2))

                    break
                elif curr_call>=sell_point_high_call:
            
                    call = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(sell_point_high_call-.2,2)
                            ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gfd', jsonify=True)
        

                    x = refresh_call()
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(round((put_percentage) + (((x-CALL)/CALL)*100),2),"\t\t",current_time)
                    total_prof.append(round((put_percentage) + (((x-CALL)/CALL)*100),2))
                    break

        


    def monitor_put(call_percentage, check):

        run = 0
        if check == 1:

            while run>=0:

                run+=1
                curr_put = refresh_put()
                if curr_put <= prof_low_Put:

                    put = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(sell_point_put-.2),2)
                         ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)


                    x = refresh_put()
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(round((call_percentage) + (((x-PUT)/PUT)*100),2),"\t\t",current_time)
                    total_prof.append(round((call_percentage) + (((x-PUT)/PUT)*100),2))
                    break
                elif curr_put >= prof_target_Put:

                    put = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(prof_low_Put),2)
                         ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)


                    x = refresh_put()
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(round((call_percentage) + (((x-PUT)/PUT)*100),2),"\t\t",current_time)
                    total_prof.append(round((call_percentage) + (((x-PUT)/PUT)*100),2))
                    break
        else:

            while run>=0:

                run+=1
                curr_put = refresh_put()

                if curr_put <= sell_point_put:

                    put = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(sell_point_put-.2),2)
                         ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)


                    x = refresh_put()
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(round((call_percentage) + (((x-PUT)/PUT)*100),2),"\t\t",current_time)
                    total_prof.append(round((call_percentage) + (((x-PUT)/PUT)*100),2))
                    break
                elif curr_put >= sell_point_high_put:
                    
                    put = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(sell_point_high_put-.2,2)
                         ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)


                    x = refresh_put()
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S", t)
                    print(round((call_percentage) + (((x-PUT)/PUT)*100),2),"\t\t",current_time)
                    total_prof.append(round((call_percentage) + (((x-PUT)/PUT)*100),2))
                    break



    def sell(key,check):

        
        if key == 0:
            if check == 1:

                put = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(sell_point_put-.2),2)
                                ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)
            else:
                put = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(prof_low_Put),2)
                                ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_put, optionType='put', timeInForce='gfd', jsonify=True)

            x = refresh_put()            
            monitor_call(float(((x-PUT)/PUT)*100), check)
        elif key == 1:

            if check ==1:

                call = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(sell_point_call-.2),2)
                                ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gfd', jsonify=True)
            else:
                call = robin_stocks.robinhood.orders.order_sell_option_limit(positionEffect = "close", creditOrDebit = "credit", price = round(float(prof_low_Call),2)
                                ,symbol = "SPY", quantity = quanity, expirationDate = exp_date, strike = strike_call, optionType='call', timeInForce='gfd', jsonify=True)

                                
            x = refresh_call()            
            monitor_put(float(((x-CALL)/CALL)*100), check)


    count = 0
    while count>=0:

        curr_call,curr_put = refresh_call(),refresh_put()


        if curr_call >= prof_target_Call:
            sell(1,0)
            break
        elif curr_put >= prof_target_Put:
            sell(0,0)
            break
        elif curr_call <= sell_point_call:
            sell(1,1)
            break
        elif curr_put <= sell_point_put:
            sell(0,1)
            break

    i+=1
print("\n",sum(total_prof),'\n')
print("All done\n")

