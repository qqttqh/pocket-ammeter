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

// 查询数据库获取所有 power 字段为 null 的记录的 roomcode 值
$sql = "SELECT roomcode FROM powerinfo WHERE power IS NULL";
$result = $conn->query($sql);

// 将 roomcode 值存储在数组中
$roomcodes = array();
if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $roomcodes[] = $row["roomcode"];
    }
}

// 关闭连接
$conn->close();

// 将数组转换为 JSON 并返回
echo json_encode(array('roomcodes' => $roomcodes));

?>
