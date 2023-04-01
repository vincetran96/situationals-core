# Resources
# https://powershellexplained.com/2017-07-31-Powershell-regex-regular-expression/
# https://www.windowscentral.com/how-rename-multiple-files-bulk-windows-10
# https://stackoverflow.com/questions/5574648/use-regex-powershell-to-rename-files


### List files with a common pattern
# $targetDir can be $_ or $zxcv, doesn't matter
# -recurse to recursively look in sub-directories
Get-ChildItem $targetDir -recurse | Where-Object {$_.name -like "Pattern_Beginning_With*"} | Select-Object name

### List files with a common pattern, using RegEx
# List any song that begins with digits
Get-ChildItem $targetDir -recurse | Where-Object {$_.name -match "\d+\. -*"}
Get-ChildItem $targetDir | Where-Object {$_.name -match "^\d+\. "}

### Rename files with a common pattern, using RegEx
# For songs beginning with "01. ", trim that part away
Get-ChildItem $targetDir | Where-Object {$_.name -match "^\d+\. "} | Rename-Item -NewName {$_.name -replace "^\d+. ", ""}
# Another way using for loop instead of pipeline
#   and using variables to make it more understandable
$items = Get-ChildItem $targetDir | Where-Object {$_.name -match "^\d+\. "}
ForEach ($item in $items) {
    Try {
        Rename-Item -Path $item -NewName $(($item.name -replace "^\d+\. ", "")) -ErrorAction Stop
    }
    Catch [System.IO.IOException] {
        $output = "Removing Item {0}" -f $item
        Write-Host $output
        Remove-Item $item
    }
    Catch {
        Write-Host "Some other exception"
    }
}
