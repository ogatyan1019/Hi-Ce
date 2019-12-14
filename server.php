<?php
	
	// アクセスがPOSTであるかを確認する
	if($_SERVER["REQUEST_METHOD"] != "POST")
	{
		// ブラウザからHTMLページを要求された場合
		echo "悪いなのび太，このページはPOST用なんだ";
	}
	else
	{
		// フォームからPOSTによって要求された場合
		$json_string = file_get_contents('php://input'); ##今回のキモ
		$json_array = json_decode($json_string, true);
		// var_dump($json_array);

		// フォームにすべて値が記入されているかを確認する
		if( is_numeric($json_array["TEMP"]) && is_numeric($json_array["HUMI"]) && is_numeric($json_array["PRESSURE"]) && is_numeric($json_array["DI"]) && is_numeric($json_array["WBGT"]))
		{
			// 値が記入されている場合
			
			// データベースへのアクセスを試みる
			try
			{
				// DB接続準備
				$dsn = 'mysql:dbname=DBname;host=host';
				$user = 'user';
				$password = 'pass';
				$dbh = new PDO($dsn, $user, $password);

				// INSERT文を変数に格納
				$sql = "INSERT INTO Tabele (DATETIME, TEMP, HUMI, PRESSURE, DI, WBGT) VALUES (now(), :TEMP, :HUMI, :PRESSURE, :DI, :WBGT)";
			 
				// 挿入する値は空のまま、SQL実行の準備をする
				$stmt = $dbh->prepare($sql);
			 
				// 挿入する値を配列に格納する
				$params = array(':TEMP' => $json_array["TEMP"], ':HUMI' => $json_array["HUMI"], ':PRESSURE' => $json_array["PRESSURE"], ':DI' => $json_array["DI"], ':WBGT' => $json_array["WBGT"]);
			 
				// 挿入する値が入った変数をexecuteにセットしてSQLを実行
				$stmt->execute($params);
			
			}
			catch(PDOException $e)
			{
				// データベースへのアクセス例外処理
				echo "データストアに失敗しました．";
			}
		}
		else
		{
			// フォームに抜けがある場合
			echo "おいルーキー，フォームが埋まっていないぜ？";
		}
		
	}

?>

