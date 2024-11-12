<?php

// 设置响应头部
header("Access-Control-Allow-Origin: *"); // 将域名替换为你的前端应用实际部署的域名
header("Access-Control-Allow-Methods: GET, POST, OPTIONS"); // 允许的请求方法
header("Access-Control-Allow-Headers: Content-Type"); // 允许的请求头部


// 连接数据库
$host = getenv('DB_HOST');
$username = getenv('DB_USERNAME');
$password = getenv('DB_PASSWORD');
$database = getenv('DB_DATABASE');

// 创建连接
$conn = new mysqli($host, $username, $password, $database);

// 检查连接是否成功
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// 查询数据库中是否存在该房间号的记录
$sql = "SELECT * FROM powerinfo WHERE roomcode='$roomcode'";
$result = $conn->query($sql);

// 初始化响应数组
$response = array();

// 如果查询到记录，则获取该记录的数据
if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    // 将查询到的数据添加到响应数组中
    $response['roomcode'] = $row['roomcode'];
    $response['power'] = $row['power'];
    $response['date'] = $row['date'];
    $response['dates'] = unserialize($row['dates']);
    $response['electricities'] = unserialize($row['electricities']);
} else {
    // 如果未查询到记录，则添加新记录
    $insert_sql = "INSERT INTO powerinfo (roomcode, power, date) VALUES ('$roomcode', NULL, NOW())";
    $insert_result = $conn->query($insert_sql);
    if ($insert_result === TRUE) {
        // 添加成功，将新记录的数据添加到响应数组中
        $response['roomcode'] = $roomcode;
        $response['power'] = null;
    } else {
        // 添加失败，设置响应数组为空
        $response = array();
    }
}

// 关闭数据库连接
$conn->close();

// 将响应数组转换为 JSON 格式并输出
echo json_encode($response);

?>
