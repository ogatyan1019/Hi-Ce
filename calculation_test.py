import math
from scipy import optimize,exp

def f(x,TEMP):
    PsTw=6.11*(10**((7.5*x)/(x+273.15)))
    return PsTw-0.00062*1013.25*(TEMP-x)

def g(x,HUMI):
    a=1-((x+273.15)/647.3)    
    Ps=221200*exp((-7.765*a+1.45*(a**1.5)-2.776*(a**3)-1.233*(a**6))/(1-a))
    return (HUMI/100)*Ps

def h(x,TEMP,HUMI):
    return f(x,TEMP)-g(x,HUMI)

def main():
    TEMP=30.0
    HUMI=60.0
    args_data=(TEMP,HUMI)
    Twet=optimize.fsolve(h,0,args=args_data)

    print(Twet)
    
if __name__ == '__main__':
    main()
