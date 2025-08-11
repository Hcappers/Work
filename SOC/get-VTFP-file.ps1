#Search VirusTotal for a has from a file
#Original script by Chris Shearer <23-June-2022>
#Submit a file hash to VirusTotal using a .csv file for input
#Input file format <filename>,<filehash>,<host>
#.\get-VTFR.ps1 <filename>
#Updated by Haskell Cappers <19-July-2023>

param([parameter(Mandatory = $true, Position = 0)] [string] $file)

#Test if $file exists
if(Test-Path $file){
  Write-host "$file exists"
}else{
  Write-Host "$file does not exist" -ErrorAction Stop
}
#Get your own VT API key here: https://www.virustotal.com/gui/join-us
#Prompt user to choose the VT API key to use
$apiKeyChoice = Read-Host "Choose the VT API key to use (1 or 2)"
if($apiKeyChoice -eq "1"){
  $VTApiKey = " "
}elseif ($apiKeyChoice -eq "2"){
  $VTApiKey = " "
}else{
  Write-Error "Invalid choice. Please choose 1 or 2." -ErrorAction Stop
}
Write-host "Processing $file"
#Set TLS 1.2
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
Function submit-VTHash($VTHash){
  $VTbody = @{resource = $VTHash; apikey = $VTApiKey}
  $VTresult = Invoke-RestMethod -Method GET -Uri 'https://www.virustotal.com/vtapi/v2/file/report' -Body $VTbody
  return $VTresult
}
#Get content of $file
$h = Import-csv $file -Header 'Filename', 'Hash', 'Host'
foreach($value in $h){
  $fileName = $value.FileName.Trim()
  $hash = $value.Hash.Trim()
  #Submit Hash
  if($filename -eq ""){
    exit
  }else{
    $VTresult = submit-VTHash($hash)
  }
  if($VTresult.positives -ge 1){
    $VTpct = (($VTresult.positives) / ($VTresult.total)) * 100
    $VTpct = [math]::Round($VTpct, 2)
  }
  $resource = $VTresult.resource
  $scan_date = $VTresult.scan_date
  $positives = $VTresult.positives
  $total = $VTresult.total
  $permalink = $VTresult.permalink
  #$percent = $VTpct

  "============================"    | Out-File -FilePath .\VT-results.txt -Append
  "File Name   :$filename"          | Out-File -FilePath .\VT-results.txt -Append
  "Resource    :$resource"          | Out-File -FilePath .\VT-results.txt -Append
  "Hosts       :$($value.Host)"     | Out-File -FilePath .\VT-results.txt -Append
  "Scan Date   :$scan_date"         | Out-File -FilePath .\VT-results.txt -Append
  "Positives   :$positives"         | Out-File -FilePath .\VT-results.txt -Append
  "Total Scans :$total"             | Out-File -FilePath .\VT-results.txt -Append
  "Permalink   : $permalink"        | Out-File -FilePath .\VT-results.txt -Append
  #"Percent     :$percent"          | Out-File -FilePath .\VT-results.txt -Append
}
