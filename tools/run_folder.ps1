param(
  [Parameter(Mandatory=$true)][string]$Root,
  [string]$PythonExe
)

if (-not $PythonExe) { $PythonExe = Join-Path $PSScriptRoot "..\.venv\Scripts\python.exe" }

$base = Split-Path -Parent $PSScriptRoot
$polOra = Join-Path $base "policies\oracle.json"
$polPs1 = Join-Path $base "policies\powershell.json"
$polIpc = Join-Path $base "policies\ipc.json"

$patterns = @("*.sql","*.ddl","*.pkb","*.pks","*.pkg","*.ps1","*.xml","*.txt")

Get-ChildItem -Path (Join-Path $Root '*') -Recurse -File -Include $patterns |
  ForEach-Object {
    $ext = [IO.Path]::GetExtension($_.FullName).ToLowerInvariant()
    $engine = $null
    $policy = $polOra
    switch ($ext) {
      ".ps1"       { $engine="powershell"; $policy=$polPs1; break }
      ".xml"       { $engine="ipc";        $policy=$polIpc; break }
      ".txt"       { $engine="ipc";        $policy=$polIpc; break }
      default      { $engine=$null;        $policy=$polOra; break } # autodetección para .sql/.ddl/.pk*
    }
    Write-Host "==> $($_.FullName)"
    $args = @("-m","cygd_validator.cli")
    if ($engine) { $args += @("--engine",$engine) }
    $args += @("--policy",$policy,"$($_.FullName)")
    & $PythonExe @args
    ""
  }
