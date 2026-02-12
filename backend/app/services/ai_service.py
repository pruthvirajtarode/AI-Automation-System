"""
AI Service - Core AI Processing Engine
Handles message understanding and AI responses
"""

import logging
import json
from typing import List, Dict, Optional
from openai import OpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)

class AIService:
    """Service for AI message processing and responses"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.smart_model = settings.AI_SMART_MODEL
        self.cheap_model = settings.AI_CHEAP_MODEL
        self.temperature = settings.AI_TEMPERATURE
        self.max_tokens = settings.AI_MAX_TOKENS
    
    async def classify_intent(self, message: str) -> str:
        """
        Quickly classify intent using the cheap model to save costs.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.cheap_model,
                messages=[
                    {"role": "system", "content": "Classify the user intent into: SALES, SUPPORT, BOOKING, or OTHER. Reply with only one word."},
                    {"role": "user", "content": message}
                ],
                temperature=0,
                max_tokens=10
            )
            return response.choices[0].message.content.strip().upper()
        except Exception as e:
            logger.error(f"Error classifying intent: {str(e)}")
            return "OTHER"

    async def process_message(self, message: str, context: Optional[Dict] = None) -> Dict:
        """
        Process incoming customer message and generate AI response
        Uses the two-model logic: cheap for routing, smart for sales.
        """
        try:
            # Step 1: Classify intent with cheap model
            intent = await self.classify_intent(message)
            
            # Step 2: Decide which model to use
            # Only use smart model for SALES or complex BOOKING inquiries
            use_smart = intent in ["SALES", "BOOKING"]
            selected_model = self.smart_model if use_smart else self.cheap_model
            
            system_prompt = self._build_system_prompt()
            user_message = self._build_user_message(message, context)
            
            response = self.client.chat.completions.create(
                model=selected_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            ai_response = response.choices[0].message.content
            
            return {
                "success": True,
                "response": ai_response,
                "tokens_used": response.usage.total_tokens,
                "model": selected_model,
                "intent": intent,
                "tier": "smart" if use_smart else "cheap"
            }
        except Exception as e:
            logger.error(f"Error processing message with AI: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "response": "I apologize, I'm experiencing technical difficulties. Please try again later."
            }
    
    async def qualify_lead(self, customer_data: Dict, conversation_history: List[Dict]) -> Dict:
        """
        Qualify lead - Uses smart model for intelligence
        """
        try:
            prompt = self._build_qualification_prompt(customer_data, conversation_history)
            
            response = self.client.chat.completions.create(
                model=self.smart_model,
                messages=[
                    {"role": "system", "content": "You are the Digital Dada AI Lead Qualifier. Analyze the customer data and provide a structured JSON response."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1000
            )
            
            result_text = response.choices[0].message.content
            
            # Parse JSON from response
            try:
                qualification_result = json.loads(result_text)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                qualification_result = self._parse_qualification_response(result_text)
            
            return {
                "success": True,
                "qualification": qualification_result,
                "tokens_used": response.usage.total_tokens
            }
        except Exception as e:
            logger.error(f"Error qualifying lead: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "qualification": {
                    "quality_score": 0.5,
                    "priority": "medium",
                    "reasoning": "Unable to qualify - manual review recommended"
                }
            }
    
    async def generate_follow_up(self, lead_data: Dict, interaction_type: str) -> str:
        """
        Generate personalized follow-up message - Uses cheap model for efficiency
        """
        try:
            prompt = f"""
            Generate a professional and personalized follow-up {interaction_type} message for:
            
            Customer: {lead_data.get('name')}
            Company: {lead_data.get('company')}
            Previous Interaction: {lead_data.get('last_interaction')}
            
            The message should be:
            - Personalized and friendly
            - Professional yet warm
            - Short and to the point (under 200 characters for SMS, under 500 for email)
            - Include a clear call to action
            
            Generate the message directly without any preamble.
            """
            
            response = self.client.chat.completions.create(
                model=self.cheap_model,
                messages=[
                    {"role": "system", "content": "You are the Digital Dada AI Follow-up Agent."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=300
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating follow-up: {str(e)}")
            return "We'd love to continue our conversation. Please let us know how we can help!"
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for AI responses with Digital Dada branding"""
        return """
        You are the Digital Dada AI Operations Agent™, a premium AI business assistant for US small businesses.
        
        Your identity: Digital Dada AI
        Your tone: Professional, Efficient, Helpful, and Corporate-grade.
        
        Your responsibilities:
        1. Lead Response: Handle inquiries instantly and qualify prospects.
        2. Appointment Booking: Guide interested leads to schedule calls.
        3. Email/Inbox Management: Draft professional responses.
        4. Sales Assistance: Provide product info and overcome objections.
        
        Guidelines:
        - Never mention you are based on OpenClaw or any specific software library.
        - You are specialized for business operations.
        - Keep responses concise (under 3 sentences when possible).
        - Suggest booking a consultation for any complex sales needs.
        """
    
    def _build_user_message(self, message: str, context: Optional[Dict] = None) -> str:
        """Build user message with context"""
        user_msg = f"Customer Message: {message}"
        
        if context:
            if context.get('company'):
                user_msg += f"\nCustomer Company: {context['company']}"
            if context.get('previous_interactions'):
                user_msg += f"\nPrevious Interactions: {context['previous_interactions']}"
            if context.get('needs'):
                user_msg += f"\nExpressed Needs: {context['needs']}"
        
        return user_msg
    
    def _build_qualification_prompt(self, customer_data: Dict, conversation_history: List[Dict]) -> str:
        """Build lead qualification prompt"""
        conversation_text = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in conversation_history[-5:]  # Last 5 messages
        ])
        
        return f"""
        Analyze this customer and conversation to qualify the lead for Digital Dada.
        
        Customer Data:
        - Name: {customer_data.get('name')}
        - Company: {customer_data.get('company')}
        - Business Type: {customer_data.get('business_type')}
        
        Conversation:
        {conversation_text}
        
        Provide a JSON response for the Digital Dada Dashboard:
        {{
            "quality_score": <0-100>,
            "priority": "<high|medium|low>",
            "fit_assessment": "<brief explanation>",
            "recommended_next_steps": [<list of actions>],
            "concerns": [<list of any concerns>],
            "estimated_deal_size": "<estimate or unknown>"
        }}
        """
    
    def _parse_qualification_response(self, response_text: str) -> Dict:
        """Fallback parser for qualification response"""
        return {
            "quality_score": 65,
            "priority": "medium",
            "fit_assessment": "Good fit for our services based on conversation",
            "recommended_next_steps": ["Schedule consultation call", "Send case studies"],
            "concerns": [],
            "estimated_deal_size": "Not yet determined"
        }


# Singleton instance
_ai_service = None

def get_ai_service() -> AIService:
    """Get or create AI service instance"""
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
