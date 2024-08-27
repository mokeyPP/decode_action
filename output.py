#2024-08-27 07:21:16
import requests
import json
import time
import os
import random
import hashlib
import hmac
import uuid
code="星星短剧"
ver="1.5"
envname="yuanshen_xxdj"
split_chars=['@','&','\n']
debug=False
def env(*args,**kwargs):
 def split_cookies(cookie,split_chars):
  for sep in split_chars:
   if sep in cookie:
    return cookie.split(sep)
  return[cookie]
 def scmain(cookies):
  for i,cookie in enumerate(cookies,1):
   print(f"--------开始第{i}个账号--------")
   main=yuanshen(cookie)
   main.main()
   print(f"--------第{i}个账号执行完毕--------")
 if not os.getenv(envname)and not debug:
  print(f"请先设置环境变量[{envname}]")
  exit()
 cookie=os.getenv(envname,"")
 if debug:
  cookie="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxNzk2MTA4MDQ1NjAwNjg2MDgwIiwibmJmIjoxNzE3NTEzMjA3LCJpYXQiOjE3MTc1MTMyMDd9.YRchhFbXDkBWd2PMPKAA9sndDbsFtzqudfHxLegIujA#BF561E4BEBE7FD10"
 try:
  print(requests.get("https://gitee.com/HuaJiB/yuanshen34/raw/master/pubilc.txt").text,"\n\n\n")
 except:
  print("网络异常,链接公告服务器失败(gitee)，请检查网络")
  exit()
 cookies=split_cookies(cookie,split_chars)
 account_count=len(cookies)
 print(f"一共获取到{account_count}个账号")
 print(f"=========🔔开始执行[{code}][{ver}]=========\n")
 start_time=time.time()
 if debug:
  scmain(cookies,*args,**kwargs)
 else:
  try:
   scmain(cookies,*args,**kwargs)
  except Exception as e:
   print(f"脚本执行出错: {e}")
 end_time=time.time()
 execution_time=end_time-start_time
 print(f"\n============🔔脚本[{code}]执行结束============")
 print(f"本次脚本总运行时间: {execution_time:.2f} 秒")
class yuanshen():
 def __init__(self,cookie):
  self.url="http://api.xx.xingdouduanju.com"
  self.encrykey="GE7dFXO1HscYE0LRWX1oNLX0EIyi6TkK5GiQUuFY"
  if len(cookie.split("#"))!=2:
   print("cookie格式错误")
   exit()
  self.cookie=cookie.split("#")[0]
  self.deviceid=cookie.split("#")[1]
  self.header={"Authorization":f"{self.cookie}","X-Version-Code":"105","X-Platform":"android","X-System":"13","X-Brand":"Redmi","X-Device-ID":f"{self.deviceid}","distributor-key":"xingxing","Content-Type":"application/json; charset=utf-8","Host":"api.xx.xingdouduanju.com","Connection":"Keep-Alive","Accept-Encoding":"gzip","User-Agent":"okhttp/4.9.2"}
 def _sha256(self,s):
  sign=hmac.new(self.encrykey.encode(),s.encode(),hashlib.sha256).hexdigest()
  return sign
 def _nonce(self):
  random_uuid=str(uuid.uuid4()).replace("-","")
  return random_uuid
 def _time(self):
  return(int(time.time()*1000))
 def gold_task(self,id,name):
  url=f"{self.url}/api/tasks/complete"
  self.nonce=self._nonce()
  self.time=self._time()
  if id==7:
   self.sign=self._sha256(f"{self.time}&{id}&{self.deviceid}&{self.nonce}&true")
  else:
   self.sign=self._sha256(f"{self.time}&{id}&{self.deviceid}&{self.nonce}&true")
  data={"timestamp":f"{self.time}","nonce":f"{self.nonce}","id":id,"done":True,"sign":f"{self.sign}"}
  r=requests.post(url,headers=self.header,json=data).json()
  if r["code"]==200001:
   if id==7:
    print(f"✅做任务[{id}][{name}]成功,获得现金[{r['data']['reward']}]")
   else:
    print(f"✅做任务[{id}][{name}]成功,获得金币[{r['data']['reward']}]")
   if id==5:
    time.sleep(random.randint(55,60))
   else:
    time.sleep(random.randint(15,60))
  else:
   print(f"❌️做任务[{id}][{name}]失败:[{r['message']}]")
   time.sleep(random.randint(8,15))
   if '验签' in r['message']:
    print("发生玄学错误 retrying...")
    return self.gold_task(id,name)
 def daily_task(self):
  url=f"{self.url}/api/tasks"
  r=requests.get(url,headers=self.header).json()
  id_list=[3,4,7,8,9]
  if r.get("code")==200001:
   print("🎉️获取任务列表成功！")
   task_dict={3:10,8:random.randint(8,15),9:random.randint(8,15)}
   for data in r.get("data",{}).get("tasks",[]):
    rjson=json.loads(json.dumps(data))
    if rjson.get('id')in id_list and not rjson.get('finished'):
     do_time=rjson.get('times',0)-rjson.get('completedCount',0)
     if rjson.get('id')in task_dict:
      do_time=task_dict[rjson.get('id')]
     print(f"✅开始执行任务[{rjson.get('name')}], 共执行[{do_time}]次")
     for _ in range(do_time):
      self.gold_task(rjson.get('id'),rjson.get('name'))
    else:
     print(f"❌️跳过任务[{rjson['name']}]")
  else:
   print(f"❌️获取任务失败,错误信息:{r}")
 def fuckniuzi(self):
  url=f"{self.url}/api/ranch_livestocks/info"
  r=requests.get(url,headers=self.header).json()
  if r["code"]==200001:
   print("🎉️获取牛子信息成功！")
   if r['data']['pendingLivestocks']==[]:
    print("牛子似乎有一点肾虚,没有产出红包")
    return
   for j in r['data']['pendingLivestocks']:
    id=j.get('id')
    url="http://api.xx.xingdouduanju.com/api/ranch_livestocks/collect"
    self.nonce=self._nonce()
    self.time=self._time()
    self.sign=self._sha256(f"{self.time}&{id}&{self.deviceid}&{self.nonce}")
    data={"nonce":f"{self.nonce}","timestamp":f"{self.time}","id":f"{id}","sign":f"{self.sign}"}
    r=requests.post(url,headers=self.header,json=data).json()
    if r["code"]==200001:
     print(f"✅收集红包成功,获得[{j.get('pendingAmount')}]元")
    else:
     print(f"❌️收集红包失败,错误信息:{r}")
    time.sleep(random.randint(5,10))
 def userinfo(self):
  url=f"{self.url}/api/user/profile"
  r=requests.get(url,headers=self.header).json()
  if r["code"]==200001:
   print("=========================================")
   print("查询用户信息成功")
   print(f"🎉️当前金币 [{r['data']['walletGold']['balance']}]")
   print(f"🎉️当前现金 [{r['data']['walletLuckyMoney']['balance']}]")
   if float(r['data']['walletLuckyMoney']['balance'])>=0.3:
    url="http://api.xx.xingdouduanju.com/api/market_goods?type=1"
    r=requests.get(url,headers=self.header).json()
    if r["code"]==200001:
     moneyid=r['data'][0]['id']
     url="http://api.xx.xingdouduanju.com/api/market_goods/exchange"
     self.time=self._time()
     self.nonce=self._nonce()
     self.sign=self._sha256(f"{self.time}&{moneyid}&{self.nonce}&{self.deviceid}")
     data={"timestamp":f"{self.time}","nonce":f"{self.nonce}","id":f"{moneyid}","sign":f"{self.sign}"}
     r=requests.post(url,headers=self.header,json=data).json()
     if r["code"]==200001:
      print(f"✅兑换0.3成功")
      time.sleep(3)
     else:
      print(f"❌️兑换0.3失败,错误信息:{r}")
   else:
    print(f"❌️当前现金不足0.3")
  else:
   print(f"❌️查询用户信息失败,错误信息:{r}")
 def main(self):
  print("🎉️开始执行[日常任务]")
  self.daily_task()
  print("===========================")
  print("🎉️开始执行[fuck牛子]")
  self.fuckniuzi()
  print("===========================")
  print("🎉️开始执行[兑换牛子&查询信息]")
  self.userinfo()
if __name__=='__main__':
 env()
