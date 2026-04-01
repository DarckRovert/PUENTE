param(
    [Parameter(Mandatory=$true)]
    [string]$Prompt,
    [string]$Model = "deepseek-r1:8b"
)

$body = @{
    model = $Model
    messages = @(
        @{ role = "user"; content = $Prompt }
    )
    stream = $false
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri "http://localhost:11434/api/chat" -Method Post -Body $body -ContentType "application/json"
    Write-Output $response.message.content
} catch {
    Write-Error "Error al conectar con Ollama en http://localhost:11434. Asegúrate que Ollama esté corriendo."
    Write-Error $_
}
