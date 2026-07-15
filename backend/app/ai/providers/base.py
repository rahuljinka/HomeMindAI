from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class AIProvider(ABC):
    @abstractmethod
    async def get_completion(
        self, 
        prompt: str, 
        system_prompt: str, 
        response_model: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Get completion from AI provider.
        If response_model is provided, it should return a structured response.
        """
        pass
