# Test simple para verificar que Python funciona
print("="*60)
print("TEST DE PANEL")
print("="*60)
print("Si ves esto, Python funciona correctamente.")
print("")

# Importar el panel
try:
    from panel_control import PanelControl
    print("Importación exitosa!")
    panel = PanelControl()
    print(f"IP Local: {panel.obtener_ip_local()}")
    print(f"Puerto 5000: {'EN USO' if panel.verificar_puerto() else 'LIBRE'}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
