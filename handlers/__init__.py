from .start import register_start_handlers
from .filters_commands import register_filters_handlers
from .dmfilters_commands import register_dmfilters_handlers

def register_all_handlers(bot):
    register_start_handlers(bot)
    register_filters_handlers(bot)
    register_dmfilters_handlers(bot)
    print("✅ All handlers registered successfully!")
