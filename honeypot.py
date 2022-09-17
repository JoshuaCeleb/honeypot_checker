from multiprocessing.sharedctypes import Value
import requests

contractAddress = input("Enter contract address: ")
url = "https://honeypotapi.p.rapidapi.com/api/v1/scan/"

querystring = {"factory_address":"0xcA143Ce32Fe78f1f7019d7d551a6402fC5350c73","token_b":"0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c","chain":"bsc","exchange":"Pancakeswap v2","router_address":"0x10ED43C718714eb63d5aA57B78B54704E256024E"}
querystring.update({'token_a': contractAddress})
headers = {
	"X-RapidAPI-Key": "f4e028336emsh225749ec2f8b486p1b7821jsnf9d8bf10deda",
	"X-RapidAPI-Host": "honeypotapi.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)