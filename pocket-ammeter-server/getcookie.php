<?php

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

// 查询数据库中 cookie 表的第一个记录的 cookie 字段值
$sql = "SELECT cookie FROM cookie LIMIT 1";
$result = $conn->query($sql);

// 初始化响应数组
$response = array();

// 如果查询到记录，则获取第一个记录的 cookie 值
if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    // 将 cookie 值添加到响应数组中
    $response['cookie'] = $row['cookie'];
} else {
    // 如果未查询到记录，则设置响应数组为空
    $response = array();
}

// 关闭数据库连接
$conn->close();

// 将响应数组转换为 JSON 格式并输出
echo json_encode($response);

?>
