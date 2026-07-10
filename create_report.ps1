$ErrorActionPreference = "Stop"

$csvPath = "C:\Users\Admin\CascadeProjects\sales_report_system\sales_report.csv"

$headers = "Employee,Department,Position,Plan,Fact,Applications"
$headers | Out-File -FilePath $csvPath -Encoding UTF8

$data = @(
    "Ivanov I.I.,Sales Dept,Manager,50,52,3",
    "Petrov P.P.,Sales Dept,Senior Manager,60,58,2",
    "Sidorov S.S.,Sales Dept,Manager,45,30,4",
    "Kozlov K.K.,Sales Dept,Manager,55,55,1",
    "Nikolaev N.N.,Sales Dept,Manager,40,35,2"
)

foreach ($line in $data) {
    $line | Out-File -FilePath $csvPath -Encoding UTF8 -Append
}

Write-Host "CSV file created: $csvPath" -ForegroundColor Green
