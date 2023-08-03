<!DOCTYPE html> 
<html> 
      
<head> 
    <title> 
        Web Service 
    </title>

    <style>
        table, th, td {
            border: 1px solid black;
        }

        th {
            min-width: 100px;
        }
    </style>
</head>

<?php
    function get_mahasiswa($url){
        $curl = curl_init();
        curl_setopt_array($curl, array(
        CURLOPT_URL => $url,
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTP_VERSION => CURL_HTTP_VERSION_1_1,
        CURLOPT_CUSTOMREQUEST => "GET",
        CURLOPT_HTTPHEADER => array(
            "Content-Type: application/json",
        ),
        ));
        $response = curl_exec($curl);
        curl_close($curl);
        return $response;
    }
?>
  
<body> 
      
    <h1 style="text-align:center;">Website Sekolah</h1>

    <h2>Data Siswa :</h2>

    <table>
        <tr>
            <th>NIS</th>
            <th>Nama</th>
            <th>Umur</th>
            <th>Alamat</th>
        </tr>
    
        <?php
            $requestData = get_mahasiswa("http://localhost:5010/get_data_siswa");
            $data_siswa = json_decode($requestData, true);

            foreach($data_siswa as $siswa) {
                $siswa = json_encode($siswa);
                $siswa = json_decode($siswa);
                echo "<tr>";
                    echo "<td>".$siswa->nis."</td>";
                    echo "<td>".$siswa->nama."</td>";
                    echo "<td>".$siswa->umur."</td>";
                    echo "<td>".$siswa->alamat."</td>";
                echo "</tr>";
            }
        ?>
    </table>
    <br>
        <h2>Data Mahasiswa :</h2>

    <table>
        <tr>
            <th>NIM</th>
            <th>Nama</th>
            <th>Umur</th>
            <th>Alamat</th>
        </tr>
    
        <?php
            $requestData = get_mahamahasiswa("http://localhost:5011/get_data_mahasiswa");
            $data_mahasiswa = json_decode($requestData, true);

            foreach($data_mahasiswa as $mahasiswa) {
                $mahasiswa = json_encode($mahasiswa);
                $mahasiswa = json_decode($mahasiswa);
                echo "<tr>";
                    echo "<td>".$mahasiswa->nim."</td>";
                    echo "<td>".$mahasiswa->nama."</td>";
                    echo "<td>".$mahasiswa->umur."</td>";
                    echo "<td>".$mahasiswa->alamat."</td>";
                echo "</tr>";
            }
        ?>
    </table>
</head> 
  
</html> 
