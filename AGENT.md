# AGENTE DE MONITOREO: Telegram Bot

Este bot corre como contenedor y notifica vía Telegram al operador del VPS.

## Características

- Modular: cada script puede ser activado o desactivado fácilmente
- Dockerizado: sigue el estándar del entorno
- Seguro: no expone más de lo necesario

## Funciones actuales

- Reporte fail2ban (bloqueos recientes)
- Uso de CPU, RAM, Disco y Red
- Estado de contenedores Docker

## Agregar módulos

Crear archivo `.py` en `bot/modules/` con la función:

```python
def run() -> str:
    return "Texto del módulo"
```
