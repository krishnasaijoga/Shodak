from dataclasses import dataclass, field


@dataclass
class ProviderUsage:
    provider:str
    calls:int=0
    retries:int=0
    prompt_tokens:int=0
    completion_tokens:int=0
    total_tokens:int=0


@dataclass
class UsageTracker:
    providers:dict[str,ProviderUsage]=field(default_factory=dict)

    def _get_provider(self,provider:str)->ProviderUsage:
        if provider not in self.providers:
            self.providers[provider]=ProviderUsage(provider=provider)
        return self.providers[provider]

    def record_call(self,provider:str,prompt_tokens:int=0,completion_tokens:int=0)->None:
        usage=self._get_provider(provider)
        usage.calls+=1
        usage.prompt_tokens+=prompt_tokens
        usage.completion_tokens+=completion_tokens
        usage.total_tokens+=prompt_tokens+completion_tokens

    def record_retry(self,provider:str)->None:
        usage=self._get_provider(provider)
        usage.retries+=1

    def reset(self)->None:
        self.providers.clear()


usage_tracker=UsageTracker()


def extract_token_usage(response:object)->tuple[int,int]:
    usage_metadata=getattr(response,"usage_metadata",None)
    if isinstance(usage_metadata, dict):
        prompt_tokens=int(usage_metadata.get("input_tokens",0)) or usage_metadata("prompt_tokens",0) or 0

        completion_tokens=int(usage_metadata.get("output_tokens",0)) or usage_metadata("completion_tokens",0) or 0

        return (prompt_tokens,completion_tokens)

    response_metadata=getattr(response,"response_metadata",None)

    if isinstance(response_metadata,dict):
        token_usage=response_metadata.get("token_usage",{})

        if isinstance(token_usage,dict):
            return (
                int(
                    token_usage.get("prompt_tokens",0) or 0
                ),
                int(token_usage.get("completion_tokens",0) or 0)
            )
    return (0,0)


def get_usage_summary()->dict[str,object]:
    providers={}

    total_calls=0
    total_retries=0
    total_prompt_tokens=0
    total_tokens=0
    total_completion_tokens=0

    for name,usage in usage_tracker.providers.items():
        providers[name]={
            "calls":usage.calls,
            "retries":usage.retries,
            "prompt_tokens":usage.prompt_tokens,
            "completion_tokens":usage.completion_tokens,
            "total_tokens":usage.total_tokens
        }

        total_completion_tokens+=(usage.completion_tokens)

    return {
        "total_calls":total_calls,
        "total_retries":total_retries,
        "prompt_tokens":total_prompt_tokens,
        "completion_tokens":total_completion_tokens,
        "total_tokens":total_tokens,
        "providers":providers
    }