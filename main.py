import vk
import json,time

#https://oauth.vk.com/authorize?client_id=2895443&scope=33554431&response_type=token
access_token=''
count_of_posts=50
#put '-' before group id example: group_id='-23242342'
group_id='-'
report_user_id=''

session = vk.Session(access_token)
api = vk.API(session)

is_sent=False

def ban_user(from_id,message_string,comment_id):
    global today_ban_list
    userinfo=api.users.get(user_ids=from_id)
    with open("ban_list.txt", "a") as myfile:
        myfile.write(time.strftime("%x %X")+' '+str(userinfo)+':'+message_string+'\n')
    with open("today_ban_list.txt", "a") as todayfile:
        todayfile.write(time.strftime("%x %X")+' '+str(userinfo)+':'+message_string+'\n')
    custom_group_id=group_id.replace('-','')
    api.groups.banUser(group_id=custom_group_id, user_id=from_id)
    api.wall.deleteComment(owner_id=group_id,comment_id=comment_id)
    print('ban')


def checkBadWords(from_id,message_string,check_comment_id):
    message_string=message_string.lower()
    with open('bad_words.txt', 'r') as file:
        bad_words_list = [line.rstrip('\n') for line in file]
    for bad_word in bad_words_list:
        if message_string.find(bad_word.lower())!=-1:
            print('contain'+':'+bad_word)
            ban_user(from_id,message_string,check_comment_id)
            time.sleep(1)

def getWall():
    global is_sent
    while True:
        if(int(time.strftime("%H"))==23 and int(time.strftime("%M"))>=0 and int(time.strftime("%M"))<10 and is_sent==False):
            with open('today_ban_list.txt', 'r') as todbanfile:
                today_ban_list=todbanfile.read()
            api.messages.send(user_id=report_user_id,message=today_ban_list)
            with open('today_ban_list.txt', 'w') as todbanfile:
                todbanfile.write("")
            is_sent=True
        if(int(time.strftime("%H"))==23 and int(time.strftime("%M"))>10):
        	is_sent=False
        wallist=api.wall.get(owner_id=group_id, count=count_of_posts)
        commentlist=[None]*count_of_posts
        for i in range(1,count_of_posts):
            commentlist[i]=api.wall.getComments(owner_id=group_id,post_id=wallist[i].get("id"),count=100)
            if commentlist[i][0]!=0:
                for j in range(1,commentlist[i][0]+1):
                    check_user_id=str(commentlist[i][j].get("from_id"))
                    check_comment_text=commentlist[i][j].get("text")
                    check_comment_id=commentlist[i][j].get("cid")
                    print(check_user_id+":"+check_comment_text)
                    checkBadWords(check_user_id,check_comment_text,check_comment_id)
            time.sleep(1)
        time.sleep(30)
        print('------------------------------------------------')      
        # with open('data.json', 'w') as outfile:
        #     json.dump(commentlist, outfile)
        #     print(commentlist)

def main():
    try:
        getWall()
    except Exception as e:
        time.sleep(10)
        print(e)
    finally:
        main()

if __name__ == '__main__':
    main()