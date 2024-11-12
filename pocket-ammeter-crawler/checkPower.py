# checkPower.py
from funLibrary import *

# 请求数据的 PHP 脚本 URL
get_data_url = "http://io.power.xyquan.top/checkPower1.php"
# 更新数据的 PHP 脚本 URL
update_data_url = "http://io.power.xyquan.top/checkPower2.php"

Cookie = get_cookie()

def main():
    # 获取 roomcodes 数组
    roomcodes = get_roomcodes(get_data_url)
    if roomcodes:
        # 创建一个空的 powers 列表来存储电量数据
        powers = []
        dates = []
        electricities = []
        # 遍历 roomcodes 数组
        for roomcode in roomcodes:
            # 切换到当前房间
            change_room_status = changeRoom(roomcode, Cookie)
            if change_room_status == 200:
                time.sleep(1)
                # 获取当前房间的电量
                data = getPower(Cookie)
                powers.append(data['power'])
                dates.append(data['dates'])
                electricities.append(data['electricities'])
                time.sleep(1)
                print('{}爬取完成'.format(roomcode))
            else:
                print(f"无法更改房间代码： {roomcode}")
        # 更新数据库中所有房间的电量
        if powers and dates and electricities:
            update_power(update_data_url, roomcodes, powers, dates, electricities)
        else:
            print('没有成功获取电量')
    else:
        print("没有新的房间需要更新数据。")

if __name__ == "__main__":
    main()
