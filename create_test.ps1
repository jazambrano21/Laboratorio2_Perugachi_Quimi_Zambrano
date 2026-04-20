$body = @{
    nombre = "Juan"
    apellido = "Perez"
    fecha_nacimiento = "1990-01-01"
    nacionalidad = "Espanol"
    correo_electronico = "juan@test.com"
} | ConvertTo-Json

try {
    $response = Invoke-RestMethod -Uri 'http://localhost:3000/api/autores' -Method POST -ContentType 'application/json' -Body $body
    Write-Host "Autor creado exitosamente:"
    Write-Host $response
} catch {
    Write-Host "Error creando autor:"
    Write-Host $_.Exception.Message
    if ($_.Exception.Response) {
        Write-Host "Status Code:" $_.Exception.Response.StatusCode
        Write-Host "Content:" $_.Exception.Response.GetResponseStream()
    }
}
