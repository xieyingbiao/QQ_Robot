# 该文档代码完成发送消息的操作

#data={
#	"message_type":message_type,
#	"cq_status":cq_status,
#	"cq_id":cq_id,
#	"group_id":group_id,
#	"user_id":user_id,
#	"nickname":nickname,
#	"message":message,
#	"image_url":image_url,
#	"message_status":message_status
#}

import requests
import chat_authority
from warframe.warframe_operate import warframe

# 消息发送模块主程序
def send(self_id,data):

	# 模块初始化
	api_ip="http://127.0.0.1:8080/"
	private_api="send_private_msg"
	group_api="send_group_msg"

	# 消息初始化
	message_type=data.get("message_type")
	cq_status=data.get("cq_status")
	cq_id=data.get("cq_id")
	group_id=data.get("group_id")
	user_id=data.get("user_id")
	message=data.get("message")
	image_url=data.get("image_url")

	# 建立需要发送的数据包（仅当接收到私密消息或者@自己的群消息时）
	if (message_type=="private"):
		# 检查聊天权限
		authority=chat_authority.get_authority(group_id,user_id)
		if (authority==False):
			return ""
		message_to_send=message_create(message,authority)
	#elif (message_type=="group" and cq_status):
	elif (message_type=="group"):
		#group_send_status=False
		#for i in range(len(cq_id)):
			#if (cq_id[i]==self_id):
				#group_send_status=True
		group_send_status=True
		if group_send_status:
			# 检查聊天权限
			authority=chat_authority.get_authority(group_id,user_id)
			if (authority==False):
				return ""
			message_to_send=message_create(message,authority)
			#print(message_to_send)
		else:
			return ""
	else:
		return ""

	if (message_to_send=="" or message_to_send==[]):
		return ""

	# 发送消息
	if (message_type=="private"):
		api_url=api_ip+private_api
		data={
			"user_id":user_id,
			"message":message_to_send,
			"auto_escape":False
		}
		r=requests.post(api_url,data=data)
	elif (message_type=="group"):
		api_url=api_ip+group_api
		data={
			"group_id":group_id,
			"message":"[CQ:at,qq="+str(user_id)+"]"+message_to_send,
			"auto_escape":False
		}
		r=requests.post(api_url,data=data)
	#print(r.text)

# 创建需要发送的消息
def message_create(message_from_user,authority):

	message_to_send=""
	message_check=message_from_user.split()
	if (len(message_check)<=1):
		return ""

	if (authority.get("warframe") and message_to_send==""):
		message_to_send=warframe(message_check,message_from_user)

	if (authority.get("honkai3") and message_to_send==""):
		pass

	if (authority.get("admin") and message_to_send==""):
		if (message_check[0].upper()=="ADMIN"):
			pass
		pass

	return message_to_send
