$block = @"
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
"@

Get-ChildItem -Recurse -Filter *.html | ForEach-Object {
    $p = $_.FullName
    $c = Get-Content -Raw -Encoding UTF8 $p

    # Skip if already has an icon link
    if ($c -match 'rel\s*=\s*["'']icon["'']') { return }

    # Insert after <head> (reliable)
    #$c2 = $c -replace '(<head\b[^>]*>\s*)', "`$1`r`n$block`r`n"
	$c2 = $c -replace '(<head\b[^>]*>)', "`$1`r`n$block"


    if ($c2 -ne $c) {
        [System.IO.File]::WriteAllText($p, $c2, (New-Object System.Text.UTF8Encoding($false)))
    }
}
