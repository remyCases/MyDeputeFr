from typing import Optional

from handlers.deputeHandler import scr_handler, stat_handler, vote_by_name_handler, dep_handler, ciro_handler, nom_handler
from utils.botManager import DiscordBot
from utils.cogManager import ProtectedCog
from utils.commandManager import protected_command
from utils.types import ContextT
from utils.utils import send_embeds


class DeputeCommand(ProtectedCog, name="depute"):
    """
    Cog that manages commands related to members of parliament (députés).
    """

    @protected_command(
        name="nom",
        description="Affiche les informations d'un député en fonction de son nom.",
    )
    async def nom(self, context: ContextT, last_name: str, first_name: Optional[str] = None) -> None:
        """
        Display information about a député by name.

        Parameters:
            context (ContextT): The context of the command.
            last_name (str): The last name of the député.
            first_name (Optional[str]): The optional first name of the député.
        """
        await send_embeds(context, lambda: nom_handler(last_name, first_name))

    @protected_command(
        name="stat",
        description="Affiches les statistiques de votes pour un député.",
    )
    async def stat(self, context: ContextT, last_name: str, first_name: Optional[str] = None) -> None:
        """
        Display voting statistics for a député.

        Parameters:
            context (ContextT): The context of the command.
            last_name (str): The last name of the député.
            first_name (Optional[str]): The optional first name of the député.
        """
        await send_embeds(context, lambda: stat_handler(last_name, first_name))

    @protected_command(
        name="dep",
        description="Affiche la liste des députés dans un département.",
    )
    async def dep(self, context: ContextT, code_dep: str) -> None:
        """
        Display députés for a given department.

        Parameters:
            context (ContextT): The context of the command.
            code_dep (str): Department code.
        """
        await send_embeds(context, lambda: dep_handler(code_dep))

    @protected_command(
        name="circo",
        description="Affiche le député associé à une circonscription.",
    )
    async def circo(self, context: ContextT, code_dep: str, code_circo: str) -> None:
        """
        Display a député by department and circonscription.

        Parameters:
            context (ContextT): The context of the command.
            code_dep (str): Department code.
            code_circo (str): Circonscription code.
        """
        await send_embeds(context, lambda: ciro_handler(code_dep, code_circo))

    @protected_command(
        name="scr",
        description="Affiche les informations d'un scrutin.",
    )
    async def scr(self, context: ContextT, code_ref: str) -> None:
        """
        Display info about a scrutin.

        Parameters:
            context (ContextT): The context of the command.
            code_ref (str): Reference of the scrutin.
        """
        await send_embeds(context, lambda: scr_handler(code_ref))

    @protected_command(
        name="vote",
        description="Affiche les informations pour un vote d'un député pour un un scrutin.",
    )
    async def vote(self, context: ContextT, code_ref: str, last_name: str, first_name: Optional[str] = None) -> None:
        """
        Display how a député voted in a scrutin.

        Parameters:
            context (ContextT): The context of the command.
            code_ref (str): Reference of the scrutin.
            last_name (str): The last name of the député.
            first_name (Optional[str]): The optional first name of the député.
        """
        await send_embeds(context, lambda: vote_by_name_handler(code_ref, last_name, first_name))

async def setup(bot: DiscordBot) -> None:
    """
    Setup function to add DeputeCommand cog to bot.

    Parameters:
        bot: The Discord bot instance.
    """
    await bot.add_cog(DeputeCommand(bot))
