"""
Translation management for the Community Layout Switcher application.
"""

import os
import locale
from typing import Dict

# Complete translation dictionary
TRANSLATIONS = {
    "en": {
        "app_name": "Community Layout Switcher",
        "window_title": "Community Layout Switcher",
        "layouts_tab": "Layouts",
        "effects_tab": "Effects",
        "themes_tab": "Themes",
        "select_layout": "Select Layout",
        "applying": "Applying {layout} layout...",
        "success": "Successfully applied {layout} layout",
        "error_config": "Error: Config file not found - {file}",
        "error_applying": "Error applying layout: {error}",
        "error": "Error: {error}",
        "apply": "Apply Layout",
        "about": "About",
        "quit": "Quit",
        "description_layout": "Apply the {layout} layout to your desktop.",
        "gnome": "GNOME",
        "effects_description": "Enhance your desktop with visual effects",
        "desktop_cube": "Desktop Cube",
        "desktop_cube_description": "Rotate your desktop on a 3D cube",
        "magic_lamp": "Magic Lamp",
        "magic_lamp_description": "Animated window minimizing effect",
        "windows_effects": "Windows Effects",
        "windows_effects_description": "Additional window animations",
        "desktop_icons": "Desktop Icons",
        "desktop_icons_description": "Add icons to your desktop",
        "extension_settings": "Extension Settings",
        "open_settings": "Open Settings",
        "not_installed": "Not installed",
        "install_extension": "Install Extension",
        "enable": "Enable",
        "disable": "Disable",
        "themes_description": "Customize your desktop appearance",
        "gtk_theme": "GTK Theme",
        "icon_theme": "Icon Theme",
        "shell_theme": "Shell Theme",
        "apply_theme": "Apply Theme",
        "no_themes_found": "No themes found",
        "license": "GPL-3.0 License",
        "gnome_only": "This feature is only available on GNOME",
        "user_theme_required": "User Themes extension is required to apply shell themes",
        "install_user_theme": "Install User Themes Extension",
        "theme_applied": "{theme_type} theme applied successfully",
        "error_applying_theme": "Error applying theme: {error}",
        "cancel": "Cancel",
        "applying_shell": "Applying shell theme {theme}...",
        "success_shell": "Successfully applied shell theme {theme}",
        "error_shell": "Error applying shell theme: {error}",
        "applying_gtk": "Applying GTK theme {theme}...",
        "success_gtk": "Successfully applied GTK theme {theme}",
        "error_gtk": "Error applying GTK theme: {error}",
        "applying_icons": "Applying icon theme {theme}...",
        "success_icons": "Successfully applied icon theme {theme}",
        "error_icons": "Error applying icon theme: {error}",
        "restart_required": "Restart may be required for changes to take effect",
        "shell_theme_restart": "Restart GNOME Shell to see the changes",
        "gtk_theme_restart": "Restart applications to see the changes",
        "icon_theme_restart": "Restart applications to see the changes",
        "about_title": "About Community Layout Switcher",
        "about_description": "Customize your GNOME desktop appearance",
        "quit_confirm": "Are you sure you want to quit?",
        "quit_confirm_title": "Quit Community Layout Switcher",
        "intro_title": "Welcome to Community Layout Switcher",
        "intro_message": "This tool allows you to customize your GNOME desktop with different layouts, effects, and themes. Before making changes, we recommend creating a backup of your current settings.",
        "intro_dont_show": "Don't show this again",
        "backup_created": "Backup created successfully",
        "backup_error": "Error creating backup: {error}",
        "backup_before_apply": "Create backup before applying layout?",
        "backup_restore": "Restore from backup",
        "backup_restore_title": "Restore Previous Settings",
        "backup_restore_message": "Are you sure you want to restore your previous settings? This will undo any changes made since the last backup.",
        "backup_restore_success": "Settings restored successfully",
        "backup_restore_error": "Error restoring backup: {error}",
        "test_layout": "Test Layout",
        "test_layout_title": "Test Layout",
        "test_layout_message": "Do you want to test this layout before applying it permanently? You can revert changes if needed.",
        "test_layout_keep": "Keep Changes",
        "test_layout_revert": "Revert Changes",
        "extensions_disabled": "GNOME Shell extensions are disabled",
        "extensions_enable_prompt": "Do you want to enable GNOME Shell extensions to apply this layout? Some layouts require extensions to function properly.",
        "extensions_enabled_success": "GNOME Shell extensions have been enabled. A restart of GNOME Shell may be required for changes to take effect.",
        "extensions_enable_error": "Error enabling GNOME Shell extensions: {error}",
        "close": "Close",
        "skip": "Skip",
        "backup": "Backup",
        "unknown": "Unknown error"
    },
    "es": {
        "app_name": "Community Layout Switcher",
        "window_title": "Community Layout Switcher",
        "layouts_tab": "Diseños",
        "effects_tab": "Efectos",
        "themes_tab": "Temas",
        "select_layout": "Seleccionar Diseño",
        "applying": "Aplicando diseño {layout}...",
        "success": "Diseño {layout} aplicado con éxito",
        "error_config": "Error: Archivo de configuración no encontrado - {file}",
        "error_applying": "Error al aplicar el diseño: {error}",
        "error": "Error: {error}",
        "apply": "Aplicar Diseño",
        "about": "Acerca de",
        "quit": "Salir",
        "description_layout": "Aplica el diseño {layout} a tu escritorio.",
        "gnome": "GNOME",
        "effects_description": "Mejora tu escritorio con efectos visuales",
        "desktop_cube": "Cubo de Escritorio",
        "desktop_cube_description": "Rota tu escritorio en un cubo 3D",
        "magic_lamp": "Lámpara Mágica",
        "magic_lamp_description": "Efecto animado de minimización de ventanas",
        "windows_effects": "Efectos de Ventanas",
        "windows_effects_description": "Animaciones adicionales de ventanas",
        "desktop_icons": "Iconos del Escritorio",
        "desktop_icons_description": "Añade iconos a tu escritorio",
        "extension_settings": "Configuración de Extensiones",
        "open_settings": "Abrir Configuración",
        "not_installed": "No instalado",
        "install_extension": "Instalar Extensión",
        "enable": "Activar",
        "disable": "Desactivar",
        "themes_description": "Personaliza la apariencia de tu escritorio",
        "gtk_theme": "Tema GTK",
        "icon_theme": "Tema de Iconos",
        "shell_theme": "Tema del Shell",
        "apply_theme": "Aplicar Tema",
        "no_themes_found": "No se encontraron temas",
        "license": "Licencia GPL-3.0",
        "gnome_only": "Esta función solo está disponible en GNOME",
        "user_theme_required": "Se requiere la extensión User Themes para aplicar temas del shell",
        "install_user_theme": "Instalar Extensión User Themes",
        "theme_applied": "Tema {theme_type} aplicado con éxito",
        "error_applying_theme": "Error al aplicar el tema: {error}",
        "cancel": "Cancelar",
        "applying_shell": "Aplicando tema del shell {theme}...",
        "success_shell": "Tema del shell {theme} aplicado con éxito",
        "error_shell": "Error al aplicar el tema del shell: {error}",
        "applying_gtk": "Aplicando tema GTK {theme}...",
        "success_gtk": "Tema GTK {theme} aplicado con éxito",
        "error_gtk": "Error al aplicar el tema GTK: {error}",
        "applying_icons": "Aplicando tema de iconos {theme}...",
        "success_icons": "Tema de iconos {theme} aplicado con éxito",
        "error_icons": "Error al aplicar el tema de iconos: {error}",
        "restart_required": "Es posible que sea necesario reiniciar para que los cambios surtan efecto",
        "shell_theme_restart": "Reinicie GNOME Shell para ver los cambios",
        "gtk_theme_restart": "Reinicie las aplicaciones para ver los cambios",
        "icon_theme_restart": "Reinicie las aplicaciones para ver los cambios",
        "about_title": "Acerca de Community Layout Switcher",
        "about_description": "Personaliza la apariencia de tu escritorio GNOME",
        "quit_confirm": "¿Estás seguro de que quieres salir?",
        "quit_confirm_title": "Salir de Community Layout Switcher",
        "intro_title": "Bienvenido a Community Layout Switcher",
        "intro_message": "Esta herramienta te permite personalizar tu escritorio GNOME con diferentes diseños, efectos y temas. Antes de realizar cambios, te recomendamos crear una copia de seguridad de tu configuración actual.",
        "intro_dont_show": "No mostrar esto de nuevo",
        "backup_created": "Copia de seguridad creada exitosamente",
        "backup_error": "Error al crear copia de seguridad: {error}",
        "backup_before_apply": "¿Crear copia de seguridad antes de aplicar el diseño?",
        "backup_restore": "Restaurar desde copia de seguridad",
        "backup_restore_title": "Restaurar Configuración Anterior",
        "backup_restore_message": "¿Estás seguro de que quieres restaurar tu configuración anterior? Esto deshará cualquier cambio realizado desde la última copia de seguridad.",
        "backup_restore_success": "Configuración restaurada exitosamente",
        "backup_restore_error": "Error al restaurar copia de seguridad: {error}",
        "test_layout": "Probar Diseño",
        "test_layout_title": "Probar Diseño",
        "test_layout_message": "¿Quieres probar este diseño antes de aplicarlo permanentemente? Puedes revertir los cambios si es necesario.",
        "test_layout_keep": "Mantener Cambios",
        "test_layout_revert": "Revertir Cambios",
        "extensions_disabled": "Las extensiones de GNOME Shell están deshabilitadas",
        "extensions_enable_prompt": "¿Quieres habilitar las extensiones de GNOME Shell para aplicar este diseño? Algunos diseños requieren extensiones para funcionar correctamente.",
        "extensions_enabled_success": "Las extensiones de GNOME Shell han sido habilitadas. Es posible que sea necesario reiniciar GNOME Shell para que los cambios surtan efecto.",
        "extensions_enable_error": "Error al habilitar las extensiones de GNOME Shell: {error}",
        "close": "Cerrar",
        "skip": "Omitir",
        "backup": "Copia de seguridad",
        "unknown": "Error desconocido"
    },
    "fr": {
        "app_name": "Community Layout Switcher",
        "window_title": "Community Layout Switcher",
        "layouts_tab": "Dispositions",
        "effects_tab": "Effets",
        "themes_tab": "Thèmes",
        "select_layout": "Sélectionner la disposition",
        "applying": "Application de la disposition {layout}...",
        "success": "Disposition {layout} appliquée avec succès",
        "error_config": "Erreur: Fichier de configuration non trouvé - {file}",
        "error_applying": "Erreur lors de l'application de la disposition: {error}",
        "error": "Erreur: {error}",
        "apply": "Appliquer la disposition",
        "about": "À propos",
        "quit": "Quitter",
        "description_layout": "Applique la disposition {layout} à votre bureau.",
        "gnome": "GNOME",
        "effects_description": "Améliorez votre bureau avec des effets visuels",
        "desktop_cube": "Cube de Bureau",
        "desktop_cube_description": "Faites pivoter votre bureau sur un cube 3D",
        "magic_lamp": "Lampe Magique",
        "magic_lamp_description": "Effet animé de réduction des fenêtres",
        "windows_effects": "Effets de Fenêtres",
        "windows_effects_description": "Animations de fenêtres supplémentaires",
        "desktop_icons": "Icônes du Bureau",
        "desktop_icons_description": "Ajoutez des icônes à votre bureau",
        "extension_settings": "Paramètres d'Extension",
        "open_settings": "Ouvrir les Paramètres",
        "not_installed": "Non installé",
        "install_extension": "Installer l'Extension",
        "enable": "Activer",
        "disable": "Désactiver",
        "themes_description": "Personnalisez l'apparence de votre bureau",
        "gtk_theme": "Thème GTK",
        "icon_theme": "Thème d'Icônes",
        "shell_theme": "Thème du Shell",
        "apply_theme": "Appliquer le Thème",
        "no_themes_found": "Aucun thème trouvé",
        "license": "Licence GPL-3.0",
        "gnome_only": "Cette fonctionnalité n'est disponible que sur GNOME",
        "user_theme_required": "L'extension User Themes est requise pour appliquer les thèmes du shell",
        "install_user_theme": "Installer l'extension User Themes",
        "theme_applied": "Thème {theme_type} appliqué avec succès",
        "error_applying_theme": "Erreur lors de l'application du thème: {error}",
        "cancel": "Annuler",
        "applying_shell": "Application du thème du shell {theme}...",
        "success_shell": "Thème du shell {theme} appliqué avec succès",
        "error_shell": "Erreur lors de l'application du thème du shell: {error}",
        "applying_gtk": "Application du thème GTK {theme}...",
        "success_gtk": "Thème GTK {theme} appliqué avec succès",
        "error_gtk": "Erreur lors de l'application du thème GTK: {error}",
        "applying_icons": "Application du thème d'icônes {theme}...",
        "success_icons": "Thème d'icônes {theme} appliqué avec succès",
        "error_icons": "Erreur lors de l'application du thème d'icônes: {error}",
        "restart_required": "Un redémarrage peut être nécessaire pour que les modifications prennent effet",
        "shell_theme_restart": "Redémarrez GNOME Shell pour voir les modifications",
        "gtk_theme_restart": "Redémarrez les applications pour voir les modifications",
        "icon_theme_restart": "Redémarrez les applications pour voir les modifications",
        "about_title": "À propos de Community Layout Switcher",
        "about_description": "Personnalisez l'apparence de votre bureau GNOME",
        "quit_confirm": "Êtes-vous sûr de vouloir quitter?",
        "quit_confirm_title": "Quitter Community Layout Switcher",
        "intro_title": "Bienvenue dans Community Layout Switcher",
        "intro_message": "Cet outil vous permet de personnaliser votre bureau GNOME avec différentes dispositions, effets et thèmes. Avant d'apporter des modifications, nous vous recommandons de créer une sauvegarde de vos paramètres actuels.",
        "intro_dont_show": "Ne plus afficher",
        "backup_created": "Sauvegarde créée avec succès",
        "backup_error": "Erreur lors de la création de la sauvegarde: {error}",
        "backup_before_apply": "Créer une sauvegarde avant d'appliquer la disposition?",
        "backup_restore": "Restaurer depuis la sauvegarde",
        "backup_restore_title": "Restaurer les paramètres précédents",
        "backup_restore_message": "Êtes-vous sûr de vouloir restaurer vos paramètres précédents? Cela annulera toutes les modifications apportées depuis la dernière sauvegarde.",
        "backup_restore_success": "Paramètres restaurés avec succès",
        "backup_restore_error": "Erreur lors de la restauration de la sauvegarde: {error}",
        "test_layout": "Tester la disposition",
        "test_layout_title": "Tester la disposition",
        "test_layout_message": "Voulez-vous tester cette disposition avant de l'appliquer de manière permanente? Vous pouvez annuler les modifications si nécessaire.",
        "test_layout_keep": "Garder les modifications",
        "test_layout_revert": "Annuler les modifications",
        "extensions_disabled": "Les extensions GNOME Shell sont désactivées",
        "extensions_enable_prompt": "Voulez-vous activer les extensions GNOME Shell pour appliquer cette disposition? Certaines dispositions nécessitent des extensions pour fonctionner correctement.",
        "extensions_enabled_success": "Les extensions GNOME Shell ont été activées. Un redémarrage de GNOME Shell peut être nécessaire pour que les modifications prennent effet.",
        "extensions_enable_error": "Erreur lors de l'activation des extensions GNOME Shell: {error}",
        "close": "Fermer",
        "skip": "Ignorer",
        "backup": "Sauvegarder",
        "unknown": "Erreur inconnue"
    },
    "de": {
        "app_name": "Community Layout Switcher",
        "window_title": "Community Layout Switcher",
        "layouts_tab": "Layouts",
        "effects_tab": "Effekte",
        "themes_tab": "Themen",
        "select_layout": "Layout auswählen",
        "applying": "Wende {layout} Layout an...",
        "success": "{layout} Layout erfolgreich angewendet",
        "error_config": "Fehler: Konfigurationsdatei nicht gefunden - {file}",
        "error_applying": "Fehler beim Anwenden des Layouts: {error}",
        "error": "Fehler: {error}",
        "apply": "Layout anwenden",
        "about": "Über",
        "quit": "Beenden",
        "description_layout": "Wende das {layout} Layout auf deinen Desktop an.",
        "gnome": "GNOME",
        "effects_description": "Verbessere deinen Desktop mit visuellen Effekten",
        "desktop_cube": "Desktop-Würfel",
        "desktop_cube_description": "Drehe deinen Desktop auf einem 3D-Würfel",
        "magic_lamp": "Magische Lampe",
        "magic_lamp_description": "Animierter Fensterminimierungseffekt",
        "windows_effects": "Fenstereffekte",
        "windows_effects_description": "Zusätzliche Fensteranimationen",
        "desktop_icons": "Desktop-Symbole",
        "desktop_icons_description": "Fügen Sie Symbole zu Ihrem Desktop hinzu",
        "extension_settings": "Erweiterungseinstellungen",
        "open_settings": "Einstellungen öffnen",
        "not_installed": "Nicht installiert",
        "install_extension": "Erweiterung installieren",
        "enable": "Aktivieren",
        "disable": "Deaktivieren",
        "themes_description": "Passe das Aussehen deines Desktops an",
        "gtk_theme": "GTK-Thema",
        "icon_theme": "Symbol-Thema",
        "shell_theme": "Shell-Thema",
        "apply_theme": "Thema anwenden",
        "no_themes_found": "Keine Themen gefunden",
        "license": "GPL-3.0 Lizenz",
        "gnome_only": "Diese Funktion ist nur unter GNOME verfügbar",
        "user_theme_required": "Die User Themes-Erweiterung ist erforderlich, um Shell-Themen anzuwenden",
        "install_user_theme": "User Themes-Erweiterung installieren",
        "theme_applied": "{theme_type}-Thema erfolgreich angewendet",
        "error_applying_theme": "Fehler beim Anwenden des Themas: {error}",
        "cancel": "Abbrechen",
        "applying_shell": "Wende Shell-Thema {theme} an...",
        "success_shell": "Shell-Thema {theme} erfolgreich angewendet",
        "error_shell": "Fehler beim Anwenden des Shell-Themas: {error}",
        "applying_gtk": "Wende GTK-Thema {theme} an...",
        "success_gtk": "GTK-Thema {theme} erfolgreich angewendet",
        "error_gtk": "Fehler beim Anwenden des GTK-Themas: {error}",
        "applying_icons": "Wende Symbol-Thema {theme} an...",
        "success_icons": "Symbol-Thema {theme} erfolgreich angewendet",
        "error_icons": "Fehler beim Anwenden des Symbol-Themas: {error}",
        "restart_required": "Ein Neustart kann erforderlich sein, damit die Änderungen wirksam werden",
        "shell_theme_restart": "Starten Sie GNOME Shell neu, um die Änderungen zu sehen",
        "gtk_theme_restart": "Starten Sie Anwendungen neu, um die Änderungen zu sehen",
        "icon_theme_restart": "Starten Sie Anwendungen neu, um die Änderungen zu sehen",
        "about_title": "Über Community Layout Switcher",
        "about_description": "Passen Sie die Erscheinung Ihres GNOME-Desktops an",
        "quit_confirm": "Sind Sie sicher, dass Sie beenden möchten?",
        "quit_confirm_title": "Community Layout Switcher beenden",
        "intro_title": "Willkommen bei Community Layout Switcher",
        "intro_message": "Dieses Tool ermöglicht es Ihnen, Ihren GNOME-Desktop mit verschiedenen Layouts, Effekten und Themen zu personalisieren. Bevor Sie Änderungen vornehmen, empfehlen wir Ihnen, eine Sicherungskopie Ihrer aktuellen Einstellungen zu erstellen.",
        "intro_dont_show": "Nicht mehr anzeigen",
        "backup_created": "Sicherung erfolgreich erstellt",
        "backup_error": "Fehler beim Erstellen der Sicherung: {error}",
        "backup_before_apply": "Sicherung vor dem Anwenden des Layouts erstellen?",
        "backup_restore": "Aus Sicherung wiederherstellen",
        "backup_restore_title": "Vorherige Einstellungen wiederherstellen",
        "backup_restore_message": "Sind Sie sicher, dass Sie Ihre vorherigen Einstellungen wiederherstellen möchten? Dies macht alle Änderungen rückgängig, die seit der letzten Sicherung vorgenommen wurden.",
        "backup_restore_success": "Einstellungen erfolgreich wiederhergestellt",
        "backup_restore_error": "Fehler beim Wiederherstellen der Sicherung: {error}",
        "test_layout": "Layout testen",
        "test_layout_title": "Layout testen",
        "test_layout_message": "Möchten Sie dieses Layout testen, bevor Sie es dauerhaft anwenden? Sie können die Änderungen bei Bedarf rückgängig machen.",
        "test_layout_keep": "Änderungen beibehalten",
        "test_layout_revert": "Änderungen rückgängig machen",
        "extensions_disabled": "GNOME Shell-Erweiterungen sind deaktiviert",
        "extensions_enable_prompt": "Möchten Sie GNOME Shell-Erweiterungen aktivieren, um dieses Layout anzuwenden? Einige Layouts erfordern Erweiterungen, um ordnungsgemäß zu funktionieren.",
        "extensions_enabled_success": "GNOME Shell-Erweiterungen wurden aktiviert. Ein Neustart von GNOME Shell kann erforderlich sein, damit die Änderungen wirksam werden.",
        "extensions_enable_error": "Fehler beim Aktivieren der GNOME Shell-Erweiterungen: {error}",
        "close": "Schließen",
        "skip": "Überspringen",
        "backup": "Sicherung",
        "unknown": "Unbekannter Fehler"
    },
    "pt_BR": {
        "app_name": "Community Layout Switcher",
        "window_title": "Community Layout Switcher",
        "layouts_tab": "Layouts",
        "effects_tab": "Efeitos",
        "themes_tab": "Temas",
        "select_layout": "Selecionar Layout",
        "applying": "Aplicando layout {layout}...",
        "success": "Layout {layout} aplicado com sucesso",
        "error_config": "Erro: Arquivo de configuração não encontrado - {file}",
        "error_applying": "Erro ao aplicar o layout: {error}",
        "error": "Erro: {error}",
        "apply": "Aplicar Layout",
        "about": "Sobre",
        "quit": "Sair",
        "description_layout": "Aplica o layout {layout} à sua área de trabalho.",
        "gnome": "GNOME",
        "effects_description": "Melhore sua área de trabalho com efeitos visuais",
        "desktop_cube": "Cubo da Área de Trabalho",
        "desktop_cube_description": "Gire sua área de trabalho em um cubo 3D",
        "magic_lamp": "Lâmpada Mágica",
        "magic_lamp_description": "Efeito animado de minimização de janelas",
        "windows_effects": "Efeitos de Janelas",
        "windows_effects_description": "Animações de janelas adicionais",
        "desktop_icons": "Ícones da Área de Trabalho",
        "desktop_icons_description": "Adicione ícones à sua área de trabalho",
        "extension_settings": "Configurações da Extensão",
        "open_settings": "Abrir Configurações",
        "not_installed": "Não instalado",
        "install_extension": "Instalar Extensão",
        "enable": "Ativar",
        "disable": "Desativar",
        "themes_description": "Personalize a aparência da sua área de trabalho",
        "gtk_theme": "Tema GTK",
        "icon_theme": "Tema de Ícones",
        "shell_theme": "Tema do Shell",
        "apply_theme": "Aplicar Tema",
        "no_themes_found": "Nenhum tema encontrado",
        "license": "Licença GPL-3.0",
        "gnome_only": "Este recurso está disponível apenas no GNOME",
        "user_theme_required": "A extensão User Themes é necessária para aplicar temas do shell",
        "install_user_theme": "Instalar Extensão User Themes",
        "theme_applied": "Tema {theme_type} aplicado com sucesso",
        "error_applying_theme": "Erro ao aplicar o tema: {error}",
        "cancel": "Cancelar",
        "applying_shell": "Aplicando tema do shell {theme}...",
        "success_shell": "Tema do shell {theme} aplicado com sucesso",
        "error_shell": "Erro ao aplicar o tema do shell: {error}",
        "applying_gtk": "Aplicando tema GTK {theme}...",
        "success_gtk": "Tema GTK {theme} aplicado com sucesso",
        "error_gtk": "Erro ao aplicar o tema GTK: {error}",
        "applying_icons": "Aplicando tema de ícones {theme}...",
        "success_icons": "Tema de ícones {theme} aplicado com sucesso",
        "error_icons": "Erro ao aplicar o tema de ícones: {error}",
        "restart_required": "Pode ser necessário reiniciar para que as alterações tenham efeito",
        "shell_theme_restart": "Reinicie o GNOME Shell para ver as alterações",
        "gtk_theme_restart": "Reinicie os aplicativos para ver as alterações",
        "icon_theme_restart": "Reinicie os aplicativos para ver as alterações",
        "about_title": "Sobre o Community Layout Switcher",
        "about_description": "Personalize a aparência da sua área de trabalho GNOME",
        "quit_confirm": "Tem certeza de que deseja sair?",
        "quit_confirm_title": "Sair do Community Layout Switcher",
        "intro_title": "Bem-vindo ao Community Layout Switcher",
        "intro_message": "Esta ferramenta permite personalizar sua área de trabalho GNOME com diferentes layouts, efeitos e temas. Antes de fazer alterações, recomendamos criar um backup das suas configurações atuais.",
        "intro_dont_show": "Não mostrar isso novamente",
        "backup_created": "Backup criado com sucesso",
        "backup_error": "Erro ao criar backup: {error}",
        "backup_before_apply": "Criar backup antes de aplicar o layout?",
        "backup_restore": "Restaurar do backup",
        "backup_restore_title": "Restaurar Configurações Anteriores",
        "backup_restore_message": "Tem certeza de que deseja restaurar suas configurações anteriores? Isso desfará quaisquer alterações feitas desde o último backup.",
        "backup_restore_success": "Configurações restauradas com sucesso",
        "backup_restore_error": "Erro ao restaurar backup: {error}",
        "test_layout": "Testar Layout",
        "test_layout_title": "Testar Layout",
        "test_layout_message": "Deseja testar este layout antes de aplicá-lo permanentemente? Você pode reverter as alterações se necessário.",
        "test_layout_keep": "Manter Alterações",
        "test_layout_revert": "Reverter Alterações",
        "extensions_disabled": "As extensões do GNOME Shell estão desativadas",
        "extensions_enable_prompt": "Você deseja ativar as extensões do GNOME Shell para aplicar este layout? Alguns layouts requerem extensões para funcionar corretamente.",
        "extensions_enabled_success": "As extensões do GNOME Shell foram ativadas. Pode ser necessário reiniciar o GNOME Shell para que as alterações tenham efeito.",
        "extensions_enable_error": "Erro ao ativar as extensões do GNOME Shell: {error}",
        "close": "Fechar",
        "skip": "Pular",
        "backup": "Backup",
        "unknown": "Erro desconhecido"
    },
    "pt_PT": {
        "app_name": "Community Layout Switcher",
        "window_title": "Community Layout Switcher",
        "layouts_tab": "Esquemas",
        "effects_tab": "Efeitos",
        "themes_tab": "Temas",
        "select_layout": "Selecionar Esquema",
        "applying": "A aplicar esquema {layout}...",
        "success": "Esquema {layout} aplicado com sucesso",
        "error_config": "Erro: Ficheiro de configuração não encontrado - {file}",
        "error_applying": "Erro ao aplicar o esquema: {error}",
        "error": "Erro: {error}",
        "apply": "Aplicar Esquema",
        "about": "Sobre",
        "quit": "Sair",
        "description_layout": "Aplica o esquema {layout} à sua área de trabalho.",
        "gnome": "GNOME",
        "effects_description": "Melhore a sua área de trabalho com efeitos visuais",
        "desktop_cube": "Cubo da Área de Trabalho",
        "desktop_cube_description": "Rode a sua área de trabalho num cubo 3D",
        "magic_lamp": "Lâmpada Mágica",
        "magic_lamp_description": "Efeito animado de minimização de janelas",
        "windows_effects": "Efeitos de Janelas",
        "windows_effects_description": "Animações de janelas adicionais",
        "desktop_icons": "Ícones da Área de Trabalho",
        "desktop_icons_description": "Adicione ícones à sua área de trabalho",
        "extension_settings": "Definições da Extensão",
        "open_settings": "Abrir Definições",
        "not_installed": "Não instalado",
        "install_extension": "Instalar Extensão",
        "enable": "Ativar",
        "disable": "Desativar",
        "themes_description": "Personalize a aparência da sua área de trabalho",
        "gtk_theme": "Tema GTK",
        "icon_theme": "Tema de Ícones",
        "shell_theme": "Tema do Shell",
        "apply_theme": "Aplicar Tema",
        "no_themes_found": "Nenhum tema encontrado",
        "license": "Licença GPL-3.0",
        "gnome_only": "Esta funcionalidade está apenas disponível no GNOME",
        "user_theme_required": "A extensão User Themes é necessária para aplicar temas do shell",
        "install_user_theme": "Instalar Extensão User Themes",
        "theme_applied": "Tema {theme_type} aplicado com sucesso",
        "error_applying_theme": "Erro ao aplicar o tema: {error}",
        "cancel": "Cancelar",
        "applying_shell": "A aplicar tema do shell {theme}...",
        "success_shell": "Tema do shell {theme} aplicado com sucesso",
        "error_shell": "Erro ao aplicar o tema do shell: {error}",
        "applying_gtk": "A aplicar tema GTK {theme}...",
        "success_gtk": "Tema GTK {theme} aplicado com sucesso",
        "error_gtk": "Erro ao aplicar o tema GTK: {error}",
        "applying_icons": "A aplicar tema de ícones {theme}...",
        "success_icons": "Tema de ícones {theme} aplicado com sucesso",
        "error_icons": "Erro ao aplicar o tema de ícones: {error}",
        "restart_required": "Pode ser necessário reiniciar para que as alterações tenham efeito",
        "shell_theme_restart": "Reinicie o GNOME Shell para ver as alterações",
        "gtk_theme_restart": "Reinicie as aplicações para ver as alterações",
        "icon_theme_restart": "Reinicie as aplicações para ver as alterações",
        "about_title": "Sobre o Community Layout Switcher",
        "about_description": "Personalize a aparência da sua área de trabalho GNOME",
        "quit_confirm": "Tem certeza de que deseja sair?",
        "quit_confirm_title": "Sair do Community Layout Switcher",
        "intro_title": "Bem-vindo ao Community Layout Switcher",
        "intro_message": "Esta ferramenta permite personalizar a sua área de trabalho GNOME com diferentes esquemas, efeitos e temas. Antes de fazer alterações, recomendamos criar uma cópia de segurança das suas configurações atuais.",
        "intro_dont_show": "Não mostrar isto novamente",
        "backup_created": "Cópia de segurança criada com sucesso",
        "backup_error": "Erro ao criar cópia de segurança: {error}",
        "backup_before_apply": "Criar cópia de segurança antes de aplicar o esquema?",
        "backup_restore": "Restaurar da cópia de segurança",
        "backup_restore_title": "Restaurar Configurações Anteriores",
        "backup_restore_message": "Tem certeza de que deseja restaurar as suas configurações anteriores? Isto irá desfazer quaisquer alterações feitas desde a última cópia de segurança.",
        "backup_restore_success": "Configurações restauradas com sucesso",
        "backup_restore_error": "Erro ao restaurar cópia de segurança: {error}",
        "test_layout": "Testar Esquema",
        "test_layout_title": "Testar Esquema",
        "test_layout_message": "Deseja testar este esquema antes de o aplicar permanentemente? Pode reverter as alterações se necessário.",
        "test_layout_keep": "Manter Alterações",
        "test_layout_revert": "Reverter Alterações",
        "extensions_disabled": "As extensões do GNOME Shell estão desativadas",
        "extensions_enable_prompt": "Deseja ativar as extensões do GNOME Shell para aplicar este esquema? Alguns esquemas requerem extensões para funcionar corretamente.",
        "extensions_enabled_success": "As extensões do GNOME Shell foram ativadas. Pode ser necessário reiniciar o GNOME Shell para que as alterações tenham efeito.",
        "extensions_enable_error": "Erro ao ativar as extensões do GNOME Shell: {error}",
        "close": "Fechar",
        "skip": "Ignorar",
        "backup": "Cópia de segurança",
        "unknown": "Erro desconhecido"
    }
}


class TranslationManager:
    """Manages translations"""
    
    def __init__(self):
        self._lang = self._get_system_language()
    
    def _get_system_language(self) -> str:
        """Get the system language"""
        try:
            # Try to get the language from the locale
            lang = locale.getdefaultlocale()[0]
            if lang:
                # Check if we have a translation for the full locale
                if lang in TRANSLATIONS:
                    return lang
                # Extract primary language code (e.g., 'pt' from 'pt_BR')
                primary_lang = lang.split('_')[0]
                # Check if we have a translation for the primary language
                if primary_lang in TRANSLATIONS:
                    return primary_lang
        except:
            pass
        
        # Fallback to checking environment variables
        try:
            lang = os.environ.get('LANG', '').split('.')[0]
            if lang:
                # Check if we have a translation for the full locale
                if lang in TRANSLATIONS:
                    return lang
                # Extract primary language code
                primary_lang = lang.split('_')[0]
                # Check if we have a translation for the primary language
                if primary_lang in TRANSLATIONS:
                    return primary_lang
        except:
            pass
        
        # Fallback to checking LANGUAGE environment variable
        try:
            lang = os.environ.get('LANGUAGE', '').split(':')[0]
            if lang:
                # Check if we have a translation for the full locale
                if lang in TRANSLATIONS:
                    return lang
                # Extract primary language code
                primary_lang = lang.split('_')[0]
                # Check if we have a translation for the primary language
                if primary_lang in TRANSLATIONS:
                    return primary_lang
        except:
            pass
        
        return "en"  # Default to English
    
    def _(self, text: str) -> str:
        """Translate text"""
        return TRANSLATIONS.get(self._lang, TRANSLATIONS["en"]).get(text, text)


# Translation function for global use
def _(text):
    """Global translation function"""
    return TRANSLATIONS.get(get_system_language(), TRANSLATIONS["en"]).get(text, text)


def get_system_language():
    """Get the system language"""
    try:
        # Try to get the language from the locale
        lang = locale.getdefaultlocale()[0]
        if lang:
            # Check if we have a translation for the full locale
            if lang in TRANSLATIONS:
                return lang
            # Extract primary language code (e.g., 'pt' from 'pt_BR')
            primary_lang = lang.split('_')[0]
            # Check if we have a translation for the primary language
            if primary_lang in TRANSLATIONS:
                return primary_lang
    except:
        pass
    
    # Fallback to checking environment variables
    try:
        lang = os.environ.get('LANG', '').split('.')[0]
        if lang:
            # Check if we have a translation for the full locale
            if lang in TRANSLATIONS:
                return lang
            # Extract primary language code
            primary_lang = lang.split('_')[0]
            # Check if we have a translation for the primary language
            if primary_lang in TRANSLATIONS:
                return primary_lang
    except:
        pass
    
    # Fallback to checking LANGUAGE environment variable
    try:
        lang = os.environ.get('LANGUAGE', '').split(':')[0]
        if lang:
            # Check if we have a translation for the full locale
            if lang in TRANSLATIONS:
                return lang
            # Extract primary language code
            primary_lang = lang.split('_')[0]
            # Check if we have a translation for the primary language
            if primary_lang in TRANSLATIONS:
                return primary_lang
    except:
        pass
    
    return "en"  # Default to English
