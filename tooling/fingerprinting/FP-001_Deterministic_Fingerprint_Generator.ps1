param(
    [Parameter(Mandatory = $true)]
    [string]$MarkdownFile
)

Write-Host ""
Write-Host "==============================================="
Write-Host "FP-001 Deterministic Fingerprint Generator"
Write-Host "Knowledge Infrastructure Bootstrap Kit"
Write-Host "Version 0.3"
Write-Host "==============================================="
Write-Host ""

if (-not (Test-Path $MarkdownFile)) {
    Write-Host "ERROR: File not found."
    Write-Host $MarkdownFile
    exit 1
}

$file = Get-Item $MarkdownFile
$content = Get-Content $MarkdownFile

$h1 = ($content | Where-Object { $_ -match '^# ' }).Count
$h2 = ($content | Where-Object { $_ -match '^## ' }).Count
$h3 = ($content | Where-Object { $_ -match '^### ' }).Count
$headingCount = $h1 + $h2 + $h3

Write-Host "Filename:"
Write-Host "  $($file.Name)"
Write-Host ""

Write-Host "File Size (bytes):"
Write-Host "  $($file.Length)"
Write-Host ""

Write-Host "Heading Count:"
Write-Host "  $headingCount"
Write-Host ""

Write-Host "H1 Count:"
Write-Host "  $h1"
Write-Host ""

Write-Host "H2 Count:"
Write-Host "  $h2"
Write-Host ""

Write-Host "H3 Count:"
Write-Host "  $h3"
Write-Host ""

Write-Host "Structural heading extraction successful."