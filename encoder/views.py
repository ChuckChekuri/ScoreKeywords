from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from encoder.services.transformer_base import BertEncoder, AlbertEncoder, RobertaEncoder

# Create your views here.

class EncodingAPIView(APIView):
    """
    An API view to encode text using a selected transformer encoder.
    Request JSON should include:
      - text: The text to encode.
      - model: (Optional) One of 'bert', 'albert', or 'roberta' (default: 'bert').
    """
    def post(self, request, format=None):
        text = request.data.get('text')
        model_choice = request.data.get('model', 'bert').lower()
        
        if not text:
            return Response(
                {"error": "No text provided."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Selecting the correct encoder based on model choice.
        if model_choice == 'bert':
            encoder = BertEncoder()
        elif model_choice == 'albert':
            encoder = AlbertEncoder()
        elif model_choice == 'roberta':
            encoder = RobertaEncoder()
        else:
            return Response(
                {"error": f"Unsupported model: {model_choice}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Assuming the encoder has an encode() method.
            encoded_output = encoder.encode(text)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response(
            {"encoded": encoded_output},
            status=status.HTTP_200_OK
        )
