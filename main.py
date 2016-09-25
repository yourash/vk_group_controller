import vk
import json,time

#https://oauth.vk.com/authorize?client_id=2895443&scope=33554431&response_type=token
access_token=''
count_of_posts=50
#put '-' before group id example: group_id='-23242342'
#пишите '-' перед номером группы пример: group_id='-23242342'
group_id='-'

session = vk.Session(access_token)
api = vk.API(session)

def ban_user(from_id,message_string,comment_id):
    userinfo=api.users.get(user_ids=from_id)
    with open("ban_list.txt", "a") as myfile:
        myfile.write(str(userinfo)+':'+message_string+'\n')
    custom_group_id=group_id.replace('-','')
    api.groups.banUser(group_id=custom_group_id, user_id=from_id)
    api.wall.deleteComment(owner_id=group_id,comment_id=comment_id)


def checkBadWords(from_id,message_string,check_comment_id):
    message_string=message_string.lower()
    with open('bad_words.txt', 'r') as file:
        bad_words_list = [line.rstrip('\n') for line in file]
    for bad_word in bad_words_list:
        if message_string.find(bad_word.lower())!=-1:
            print('contain'+':'+bad_word)
            ban_user(from_id,message_string,check_comment_id)

def main():
    while True:
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

if __name__ == '__main__':
    main()