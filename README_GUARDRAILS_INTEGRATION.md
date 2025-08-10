# Guardrails Integration for Pilar2

## Overview

This document describes the integration of **Guardrails** into the Pilar2 system to provide AI response validation, quality control, and compliance monitoring. **All validation errors have been resolved and the system is fully operational with CrewAI integration.**

## 🔧 Recent Fixes

### Dependencies Issue Resolution ✅
- **Problem**: `serper-dev` package caused installation errors
- **Solution**: Removed non-existent package from all dependency files
- **Result**: Clean installation without errors
- **Note**: All Guardrails functionality remains fully operational

## What is Guardrails?

Guardrails is a framework that helps ensure AI responses meet specific quality standards, compliance requirements, and safety guidelines. In Pilar2, it's used to:

- **Validate AI responses** for accuracy and completeness
- **Ensure compliance** with OECD Pillar Two regulations
- **Monitor quality** of tax advice and analysis
- **Provide fallback validation** when AI validation fails
- **Track response metrics** for continuous improvement

## Key Features

### 1. **AI Response Validation**
- Automatic validation of all AI-generated responses
- Quality scoring based on multiple criteria
- Content format and structure validation
- Professional language assessment

### 2. **Pillar Two Compliance**
- Specific validation for tax compliance questions
- Risk level assessment (Low, Medium, High, Critical)
- Compliance status tracking
- Regulatory requirement verification

### 3. **Quality Control**
- Configurable quality thresholds
- Automatic response improvement
- Warning system for low-quality responses
- Performance monitoring and metrics

### 4. **Multi-language Support**
- English and Hebrew validation
- Language-specific pattern recognition
- Cultural context awareness

## Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   User Query   │───▶│ EnhancedQAEngine │───▶│ Guardrails     │
│                 │    │                  │    │ Service        │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │   AI Response    │    │   Validation    │
                       │                  │    │   Result        │
                       └──────────────────┘    └─────────────────┘
```

## Installation

### 1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

### 2. **Verify Installation**
```python
from backend.services.guardrails_service import GuardrailsService

# Test if Guardrails is available
service = GuardrailsService()
print(f"Guardrails available: {service.guardrails_available}")
```

## Configuration

### 1. **Main Configuration File**
Edit `config/guardrails_config.yaml` to customize:

```yaml
quality_control:
  min_threshold: 0.8  # Minimum quality score
  max_response_length: 2000
  
pillar_two_validation:
  enabled: true
  valid_compliance_statuses:
    - compliant
    - non_compliant
    - requires_review
    - unknown
```

### 2. **Environment Variables**
```bash
# Optional: Override default settings
export GUARDRAILS_QUALITY_THRESHOLD=0.9
export GUARDRAILS_MAX_LENGTH=3000
```

## Usage Examples

### 1. **Basic Validation**
```python
from backend.services.guardrails_service import GuardrailsService

service = GuardrailsService()

# Validate a response
result = service.validate_ai_response(
    response="Your AI response here",
    question_type="compliance"
)

print(f"Quality Score: {result['quality_score']}")
print(f"Warnings: {result['warnings']}")
```

### 2. **Enhanced QA with Guardrails**
```python
from backend.services.enhanced_qa_engine import EnhancedQAEngine

engine = EnhancedQAEngine()

# Ask a question (automatically validated)
response = engine.ask_enhanced_question(
    "What are the compliance requirements for Pillar Two?",
    language="en"
)

# Access validation results
validation = response['guardrails_validation']
print(f"Compliance Status: {validation['compliance_status']}")
print(f"Risk Level: {validation['risk_level']}")
```

### 3. **Manual Validation**
```python
# Validate existing responses
validation_result = engine.validate_response_manually(
    response="Existing response text",
    question_type="regulatory"
)
```

## Validation Results

### Response Structure
```python
{
    "success": True,
    "original_response": "Original AI response",
    "validated_response": "Validated/improved response",
    "validation_details": {
        "method": "guardrails",
        "compliance_status": "compliant",
        "risk_level": "low",
        "confidence": 0.85
    },
    "quality_score": 0.85,
    "warnings": [],
    "timestamp": "2024-01-01T12:00:00"
}
```

### Quality Score Breakdown
- **0.0-0.3**: Poor quality, significant issues
- **0.4-0.6**: Below average, needs improvement
- **0.7-0.8**: Acceptable quality
- **0.9-1.0**: High quality, meets standards

## Monitoring and Metrics

### 1. **Service Status**
```python
status = engine.get_guardrails_status()
print(f"Guardrails Available: {status['guardrails_available']}")
print(f"Quality Threshold: {status['quality_threshold']}")
```

### 2. **Performance Metrics**
- Response validation time
- Quality score distribution
- Warning frequency
- Compliance status trends

## Error Handling

### 1. **Fallback Mode**
When Guardrails is unavailable:
- Automatic fallback to basic validation
- Quality scoring using regex patterns
- Warning about reduced validation

### 2. **Error Recovery**
- Graceful degradation on validation failures
- Detailed error logging
- User notification of issues

## Best Practices

### 1. **Question Classification**
- Use specific question types for better validation
- Leverage Pillar Two patterns for compliance questions
- Consider language context for Hebrew responses

### 2. **Quality Thresholds**
- Start with default threshold (0.8)
- Adjust based on your compliance requirements
- Monitor false positive/negative rates

### 3. **Response Monitoring**
- Regularly review validation warnings
- Track quality score trends
- Use metrics for continuous improvement

## Troubleshooting

### Common Issues

#### 1. **Guardrails Not Available**
```
Warning: Guardrails not available. AI validation will be disabled.
```
**Solution**: Install required dependencies
```bash
pip install guardrails-ai pydantic jsonschema marshmallow
```

#### 2. **Low Quality Scores**
- Check response length and structure
- Verify professional terminology usage
- Review compliance status patterns

#### 3. **Validation Errors**
- Check response format and content
- Verify question type classification
- Review error logs for details

### Debug Mode
```python
import logging
logging.basicConfig(level=logging.DEBUG)

# Enable detailed logging
logger = logging.getLogger('backend.services.guardrails_service')
logger.setLevel(logging.DEBUG)
```

## Performance Considerations

### 1. **Caching**
- Enable response caching for repeated validations
- Configure appropriate TTL values
- Monitor memory usage

### 2. **Concurrent Processing**
- Limit concurrent validations based on system resources
- Use async processing for high-volume scenarios
- Monitor response times

### 3. **Resource Optimization**
- Regular cleanup of validation caches
- Monitor API usage and costs
- Optimize validation patterns

## Security and Compliance

### 1. **Data Privacy**
- No sensitive data stored in validation logs
- Secure handling of compliance information
- Audit trail for validation decisions

### 2. **Regulatory Compliance**
- OECD Pillar Two compliance validation
- Risk assessment and mitigation
- Professional standards enforcement

## Future Enhancements

### Planned Features
- **Advanced Pattern Recognition**: Machine learning-based validation
- **Custom Validation Rules**: User-defined validation criteria
- **Real-time Monitoring**: Live validation dashboard
- **Integration APIs**: External validation service support

### Contributing
- Report bugs and feature requests
- Submit validation rule improvements
- Contribute to pattern recognition
- Help with language support

## Support

For technical support or questions about Guardrails integration:

1. **Check the logs** for detailed error information
2. **Review configuration** for proper setup
3. **Test with simple examples** to isolate issues
4. **Consult documentation** for usage patterns

## License

This Guardrails integration is part of the Pilar2 project and follows the same licensing terms.
