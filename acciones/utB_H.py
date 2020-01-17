"""
Rutinas de Utilidad para analizar los precios de la acciones: B&H entre dos fechas
	Evaluacion de parámetros
	
	Nº de dias
	CAGR: Rendimiento anual compuesto
	std_Y: volatilidad o desviacion típica anualizada
	MaxDD: Maxima caida de la serie
	Sharpe: ratio CAGR / std_Y
	CAR: ratio    CAGR / MaxDD
	UI: Ulcer index
	Sortino: ratio """

import pandas as pd
import numpy as np
import datetime 
import matplotlib.pyplot as plt

# Get Maximum DrawDown & [optional] Visualize Drawdown of a Series or of a whole dataframe [autodetect]
#######################################################################################################
def Get_Drawdown(pC,ShowPlot=False):
    # Roll_Max = pC.rolling(252, min_periods=1).max() # Cálculo teniendo en cuenta solo los datos del ultimo año
    Roll_Max = pC.cummax() # maximum.accumulate
    daily_drawdown = pC/Roll_Max - 1.0
    MaxDD = daily_drawdown.min()
    
    # Plot the results
    if(ShowPlot):
        if(isinstance(pC, pd.Series)):
            LienzoY = 12
        else:
            if(isinstance(pC, pd.DataFrame)):
                ncols=pC.columns.size
                LienzoY= 2*ncols
        fig, ax1  = plt.subplots(figsize=(15,LienzoY)) #plt.subplots(figsize=(15,18))
        Gcolor='tomato'
        ax1.set_ylabel('Drawdown [%]', color=Gcolor)
        ax1.tick_params(axis='y', labelcolor=Gcolor)
        if(isinstance(pC, pd.Series)):
            ax1.set_ylim(max(300*MaxDD,-100), 0) # escalamos el segundo eje para que el Drawdonw ocupe 1/3 del espacio
            ax1.fill_between(daily_drawdown.index,100*daily_drawdown,0,color=Gcolor)
        (100*daily_drawdown).plot(ax=ax1,lw=1.,subplots=True,color='red')
        # Show the plot
        plt.grid(True)
        plt.show()
    
    #print('MaxDD=',round(100*MaxDD,2),'%')
    return MaxDD


# In[108]:

def GetParamEvaluacionSerie(pC,pC_DRet):
	# Get the number of days for the Series
	days = (pC.index[-1] - pC.index[0]).days
	#print('days=',days)
    
	# Calculate the CAGR 
	cagr = ((pC.iloc[-1] / pC.iloc[1]) ** (365.0/days)) - 1

	# Calculate annualized std
	std_D = pC_DRet.std()  # desviacion standard diaria
	std_Y = std_D * (252**0.5) # desviacion standard anualizada
	Sharpe_Y = cagr/std_Y      # sharpe ratio anual
	MaxDD = Get_Drawdown(pC)
	CAR = cagr / abs(MaxDD)    # CAR
	FInicio = pC.index[0].date() 
	FFinal = pC.index[-1].date()
	# Print the CAGR
	#print('Nº Dias=',days,' CAGR=',round(100*cagr,2),'%   std_Y=',round(100*std_Y,2), '%   MaxDD=',round(100*MaxDD,2),'% Sharpe=',round(Sharpe_Y,4),' CAR=',round(CAR,4))
	#print('Nº Dias=',days,' CAGR=',round(100*cagr,2),'%   std_Y=',round(100*std_Y,2), '% Sharpe=',round(Sharpe_Y,4))
	if(isinstance(pC, pd.DataFrame)):
		dfparam = pd.DataFrame(index=cagr.index)
		dfparam = pd.concat([FInicio,FFinal,days,cagr,std_Y,MaxDD,Sharpe_Y,CAR],axis=1,keys=['FInicio','FFinal','Ndias','cagr','std_Y','MaxDD','Sharpe_Y','CAR'])
	else:
		dfparam = pd.DataFrame(index=[pC.name],columns=['FInicio','FFinal','Ndias','cagr','std_Y','MaxDD','Sharpe_Y','CAR'])
		dfparam.iloc[0] = [FInicio,FFinal,days,cagr,std_Y,MaxDD,Sharpe_Y,CAR]
	return(dfparam)
	 
def GetParamPrecio(Ticker,pDF):
	print('GetParamPrecio\n')
	pC = pd.DataFrame(index=pDF.index)
	pC['Close'] = pd.to_numeric(pDF['Close'], errors='coerce') #.fillna(0) #.copy()
	pC['DRet'] = np.log(pC['Close']/pC['Close'].shift(1)).bfill() #pAllC_DRet = pAllC.pct_change().bfill() # menos precisa
	pC.index = pd.to_datetime(pDF['Date'])
	print(pDF.head())
	print(pC.head())
	dfEvalPrecio = GetParamEvaluacionSerie(pC['Close'],pC['DRet'])
	dfEvalPrecio.index = Ticker
	#dfEvalPrecio.index.names = ['Ticker']
	return dfEvalPrecio	 
	 
