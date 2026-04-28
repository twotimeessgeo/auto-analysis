param(
  [Parameter(Mandatory = $true)]
  [string]$VenvDir
)

$ErrorActionPreference = "SilentlyContinue"

function Test-PythonCandidate {
  param(
    [Parameter(Mandatory = $true)]
    [string]$Exe,
    [string[]]$Args = @()
  )

  try {
    $probe = "import sys; raise SystemExit(0 if sys.version_info >= (3, 10) else 1)"
    & $Exe @Args -c $probe > $null 2>&1
    if ($LASTEXITCODE -eq 0) {
      return $true
    }
  } catch {
    return $false
  }
  return $false
}

function Add-Candidate {
  param(
    [Parameter(Mandatory = $true)]
    [System.Collections.ArrayList]$Candidates,
    [Parameter(Mandatory = $true)]
    [string]$Exe,
    [string[]]$Args = @()
  )

  if ([string]::IsNullOrWhiteSpace($Exe)) {
    return
  }

  [void]$Candidates.Add([PSCustomObject]@{
    Exe = $Exe
    Args = $Args
  })
}

$candidates = [System.Collections.ArrayList]::new()

foreach ($version in @("-3.13", "-3.12", "-3.11", "-3.10")) {
  Add-Candidate -Candidates $candidates -Exe "py" -Args @($version)
}
Add-Candidate -Candidates $candidates -Exe "python"
Add-Candidate -Candidates $candidates -Exe "python3"

$registryPatterns = @(
  "HKCU:\Software\Python\PythonCore\*\InstallPath",
  "HKLM:\Software\Python\PythonCore\*\InstallPath",
  "HKLM:\Software\WOW6432Node\Python\PythonCore\*\InstallPath",
  "HKCU:\Software\Python\*\*\InstallPath",
  "HKLM:\Software\Python\*\*\InstallPath",
  "HKLM:\Software\WOW6432Node\Python\*\*\InstallPath"
)

foreach ($pattern in $registryPatterns) {
  foreach ($key in Get-Item -Path $pattern) {
    $installPath = $key.GetValue("")
    if (-not [string]::IsNullOrWhiteSpace($installPath)) {
      $exePath = Join-Path $installPath "python.exe"
      if (Test-Path $exePath) {
        Add-Candidate -Candidates $candidates -Exe $exePath
      }
    }
  }
}

$commonPatterns = @(
  "$env:LOCALAPPDATA\Programs\Python\Python*\python.exe",
  "$env:ProgramFiles\Python*\python.exe",
  "${env:ProgramFiles(x86)}\Python*\python.exe",
  "C:\Python*\python.exe"
)

foreach ($pattern in $commonPatterns) {
  foreach ($path in Get-ChildItem -Path $pattern | Sort-Object FullName -Descending) {
    Add-Candidate -Candidates $candidates -Exe $path.FullName
  }
}

$seen = @{}
$found = $null
foreach ($candidate in $candidates) {
  $key = "$($candidate.Exe)|$($candidate.Args -join " ")"
  if ($seen.ContainsKey($key)) {
    continue
  }
  $seen[$key] = $true

  if (Test-PythonCandidate -Exe $candidate.Exe -Args $candidate.Args) {
    $found = $candidate
    break
  }
}

if ($null -eq $found) {
  Write-Host "Python 3.10 이상을 찾지 못했습니다."
  exit 1
}

$display = $found.Exe
if ($found.Args.Count -gt 0) {
  $display = "$display $($found.Args -join " ")"
}
Write-Host "사용할 Python: $display"

$venvArgs = @()
$venvArgs += $found.Args
$venvArgs += @("-m", "venv", $VenvDir)
& $found.Exe @venvArgs
if ($LASTEXITCODE -ne 0) {
  Write-Host "Python 가상환경을 만들지 못했습니다."
  exit 1
}

exit 0
