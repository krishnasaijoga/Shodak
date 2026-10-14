class ShodakApiError(Exception):
    def __init__(
        self,
        error:str,
        message:str,
        status_code:int=500
    )->None:
        super().__init__(message)

        self.error=error
        self.message=message
        self.status_code=status_code


class LlmProviderUnavailableError(ShodakApiError):
    def __init__(self, message:str="No Configured LLM provider is currently available.")->None:
        super().__init__(error="llm_provider_unavailable", message=message, status_code=503)


class WorkflowExecutionError(ShodakApiError):
    def __init__(self, message:str="The Shodak workflow could not complete successfully.")->None:
        super().__init__(
            error="workflow_execution_failed",
            message=message,
            status_code=500
        )