# # create views here
from flask import request, make_response, jsonify
from flask.views import MethodView
from . import models
from app import db
import pandas as pd
#Endpoint for getting a trade by id
class TradesIDAPI(MethodView):
  def get(self,id):
    #Return the first matched id found in DB
    trade = models.Trades.query.filter_by(id=id).first()
    #If match found, return the trade
    if trade:
      return {"id":trade.id,"type":trade.trade_type,"user_id":trade.user_id,
      "symbol":trade.symbol,"shares":trade.shares,"timestamp":trade.timestamp,"price":trade.price}
    #Else return 404 not found
    else:
      return "Trade with the requested id doesn't exist",404
  
  #Unimplemented method belows since trades do not support put,patch,delete
  def put(self,id):
    return "Method not allowed",405

  def patch(self,id):
    return "Method not allowed",405

  def delete(self,id):
    return "Method not allowed",405

#Endpoint for get and post methods for trades API
class TradesAPI(MethodView):
  def get(self):
    #Declaring user_id and trade_type to be used if they are passed in
    user_id, trade_type = None,None
    #List to hold the results of the query
    trade_results = []

    #Bind user_id and type to variables declared above if one or both exist
    if "user_id" in request.args:
      user_id = request.args["user_id"]
    if "type" in request.args:
      trade_type = request.args["type"]
    
    #Base query for the table
    trades = models.Trades.query

    #Filter query with optional parameters if they are in fact passed in
    if user_id:
      trades = trades.filter_by(user_id=user_id)
    if trade_type:
      trades = trades.filter_by(trade_type=trade_type)

    #Gather results of query
    results = trades.all()

    #Iterate through results and build response, if the flask restful library was used 
    # we could take advantage of response marshalling and avoid the iteration
    for trade in results:
      trade_results.append({"id":trade.id,"type":trade.trade_type,"user_id":trade.user_id,
      "symbol":trade.symbol,"shares":trade.shares,"timestamp":trade.timestamp,"price":trade.price})
    
    #If we have results return else return an empty list
    if trade_results:
      return jsonify(trade_results),200
    else:
      return "[]",200

  def post(self):
    args = request.json
    #Extracting parameters from the request object
    trade_type = args['type']
    user_id = args['user_id']
    symbol = args['symbol']
    shares = args['shares']
    timestamp = args['timestamp']
    price = args['price']

    #If trade type invalid, or if shares are out of bounds [1,100] return 400 error and response
    if trade_type == "INVALID":
      return make_response(("Invalid Shares",400))
    elif shares > 100 or shares < 1:
      return make_response(("Number of shares is invalid",400))
    #else create a new trades object that we then add and commit to the database
    else:
      new_trade = models.Trades(
        trade_type=args['type'],
        user_id = args['user_id'],
        symbol = args['symbol'],
        shares = args['shares'],
        timestamp = args['timestamp'],
        price = args['price']
      )
      db.session.add(new_trade)
      db.session.commit()
      #Return newly created trade object with a 201 response
      trade = {"id":new_trade.id,"type":new_trade.trade_type,"user_id":new_trade.user_id,"symbol":new_trade.symbol,"shares":new_trade.shares,"timestamp":new_trade.timestamp,"price":new_trade.price}
      return trade,201


#Return aggregations by month
#Takes in settlement location name and returns
#settlement location name, start date of the month
#avg_price, avg_volume, avg_total_dollars, min_price, max_price
#If no settlement is given return above calculations for all settlements
# class AggMonthly(MethodView):
#   def get(self):
#     df = models.df
#     settlement_location = None
#     if "settlement_location" in request.args:
#       settlement_location = request.args["settlement_location"]
    
#     if settlement_location:
#       df = models.df.loc[(models.df['SettlementLocationName'] == settlement_location)]

#     #Since there is only one entry per month in the dataset, we can assume that that will be the avg_price and avg_volume
#     #But if we didn't want to make that assumption, we could do something like the following
#     results = []
#     #Columns we want to average
#     df.index = pd.to_datetime(df['DateOfService'],format='%m/%d/%y %I:%M%p')
#     df_avgs = df["PricePerMWh","VolumeMWh"].groupby(by=[df.index.month, df.index.year,df.SettlementLocationName]).agg({'vals': ['mean', 'min', 'max']})
#     for row in df_avgs.iterrows():
#       results.append({
#         "settlement_location": row["SettlementLocationName"],
#         "settlement_location_id": row["SettlementLocationId"],
#         "month_date": row["DateOfService"], #Its always the first of the month in dataset
#         "avg_price": row["mean"],
#         "avg_volume":row["VolumeMWh"],
#         "avg_total_dollars": "ada",
#         "min_price":row["min"],
#         "max_price": row["max"]
#       }
#       )


# #Return Values for Settlement Location
# #API takes in settlement location, start date, end_date
# #Return single settlement location name, id, date of service, price per mwh, volume mwh
# #if no settlement location given return all settlement locations
# class RetSettlement(MethodView):
#   def get(self,start_date,end_date):
#     df = models.df
#     settlement_location = None
#     if settlement_location in request.args:
#       settlement_location = request.args["settlement_location"]

#     if settlement_location:
#       df = models.df.loc[(models.df['SettlementLocationName'] == settlement_location) & 
#       (models.df["DateOfService"] >= start_date) & (df["DateOfService"] <= end_date)]
#     else:
#       df = models.df.loc[(models.df["DateOfService"] >= start_date) & (models.df["DateOfService"] <= end_date)]

#     results = []
#     for row in df.iterrows():
#       results.append({
#         "settlement_location": row["SettlementLocationName"],
#         "settlement_location_id": row["SettlementLocationId"],
#         "date_of_service": row["DateOfService"],
#         "price_per_mwh": row["PricePerMWh"],
#         "volume_mwh":row["VolumeMWh"]
#       })
#     return results,200

