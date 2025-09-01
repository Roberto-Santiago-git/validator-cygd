param(
  [Parameter(Mandatory=$true)][string]$PythonExe,
  [Parameter(Mandatory=$true)][string]$Policy,
  [string]$Engine
)
$ok = $true
foreach ($f in $args) {
  $cmd = @("-m","cygd_validator.cli","--policy",$Policy)
  if ($Engine) { $cmd += @("--engine",$Engine) }
  $cmd += $f
  & $PythonExe @cmd
  if ($LASTEXITCODE -ne 0) { $ok = $false }
}
if (-not $ok) { exit 1 }
