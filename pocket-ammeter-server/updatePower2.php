<?php

// 解析 POST 请求中的 JSON 数据
$json_data = json_decode(file_get_contents('php://input'), true);

// 连接数据库
$host = getenv('DB_HOST');
$username = getenv('DB_USERNAME');
$password = getenv('DB_PASSWORD');
$database = getenv('DB_DATABASE');

// 创建连接
$conn = new mysqli($host, $username, $password, $database);

// 检查连接是否成功
if ($conn->connect_error) {
    die("连接失败：" . $conn->connect_error);
}

// 更新数据库中的数据
foreach ($json_data['roomcodes'] as $key => $roomcode) {
    // 获取对应的 power dates electricities 值
    $power = $json_data['powers'][$key];
    $dates = serialize($json_data['dates'][$key]);
    $electricities = serialize($json_data['electricities'][$key]);
    // 执行更新操作
    $sql = "UPDATE powerinfo SET power='$power', date=NOW(), dates = '$dates', electricities = '$electricities' WHERE roomcode='$roomcode'";
    $result = $conn->query($sql);

    // 检查更新是否成功
    if ($result === false) {
        echo "更新记录时出错： " . $conn->error;
        break; // 如果出现错误，终止循环
    }
}

// 关闭连接
$conn->close();

// 输出更新完成消息
echo "更新完成"
?>
