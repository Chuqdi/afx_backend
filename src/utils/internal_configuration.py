from src.models.internal_configuration import InternalConfiguration


async def get_current_internal_configuration():
    """
    Retrieve the current internal configuration

    Notes:
    - new campaigns are created from this configuration

    Returns:
    - configuration(InternalConfiguration): The most newest of the configurations
    """
    recent_configurations = (
        await InternalConfiguration.find().limit(1).sort("-created_at").to_list()
    )
    return recent_configurations[0]
