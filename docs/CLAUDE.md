# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NetCop Hub is a Django-based AI agent marketplace that allows users to purchase and use various AI-powered agents for tasks like social media ad generation, data analysis, weather reporting, and more. The system features a wallet-based payment system with Stripe integration using API-based payment verification for reliable, instant transactions.

### Project Structure
```
netcop_django/
├── 📁 docs/              # All documentation, guides, and logs
├── 📁 tests/             # All test files and scripts
├── 📁 agent_base/        # Agent framework and creation tools
├── 📁 authentication/    # User management system
├── 📁 core/              # Main app (homepage, marketplace, wallet)
├── 📁 wallet/            # Payment and transaction system
├── 📁 weather_reporter/  # Example individual agent app
│   └── templates/        # Agent-specific templates (namespaced)
│       └── weather_reporter/
│           └── detail.html
├── 📁 templates/         # Global templates (core, auth)
├── 📁 static/            # Static assets (CSS, JS, images)
├── 📁 media/             # User-uploaded files
├── 📁 netcop_hub/        # Django project configuration
└── manage.py             # Django management commands
```

## Key Architecture Components

### Individual Agent Architecture
The project uses a modular individual agent architecture where each agent is a separate Django app:

- **Base Framework**: `agent_base/` provides common functionality:
  - `BaseAgent` model for agent marketplace catalog
  - `BaseAgentRequest`/`BaseAgentResponse` abstract models for tracking
  - `BaseAgentProcessor` abstract class for webhook handling
  - `BaseAgentView` abstract class for form processing and authentication

- **Individual Agent Apps**: Each agent has its own app (`agent_social_ads/`, `agent_weather/`, etc.):
  - Custom models extending base classes
  - Specialized processors for webhook communication
  - Individual views and URL routing
  - Separate templates and static files

### Webhook Processing System
All agents communicate with external AI services via N8N webhooks:
- Processors handle data preparation, request/response processing
- Webhook URLs configured via environment variables
- Built-in error handling and timeout management
- Processing time tracking and logging

### User Authentication & Wallet System
- Custom User model with wallet balance functionality
- Stripe integration for payments (`wallet/stripe_handler.py`)
- Transaction tracking via `WalletTransaction` model
- **IMPORTANT**: Wallet deduction happens ONLY after successful processing (not before)
- Real-time balance updates in frontend after successful agent execution

## Essential Commands

### Development Setup
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (no requirements.txt - manual installation needed)
pip install django djangorestframework python-decouple stripe requests

# Database setup
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Populate agents catalog
python manage.py populate_base_agents
```

### Running the Application
```bash
# Start development server
python manage.py runserver

# Run with specific settings
python manage.py runserver --settings=netcop_hub.settings
```

### Database Management
```bash
# Create new migrations
python manage.py makemigrations [app_name]

# Apply migrations
python manage.py migrate

# Reset database (if needed)
python manage.py flush

# Django shell
python manage.py shell
```

### Testing
```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test agent_social_ads

# Run with verbosity
python manage.py test --verbosity=2
```

## Environment Configuration

The project uses python-decouple for environment management. Key variables in `.env`:

### Required Settings
- `SECRET_KEY`: Django secret key
- `DEBUG`: Development mode flag
- `ALLOWED_HOSTS`: Comma-separated host list
- `DATABASE_URL`: PostgreSQL connection string (uses SQLite by default)

### Webhook Configuration
Each agent requires webhook URLs in format:
- `N8N_WEBHOOK_[AGENT_NAME]`: Django backend webhook URL
- `NEXT_PUBLIC_N8N_WEBHOOK_[AGENT_NAME]`: Frontend webhook URL

### Payment Integration
- `STRIPE_SECRET_KEY`: Stripe API secret key
- `STRIPE_WEBHOOK_SECRET`: Stripe webhook signing secret
- `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY`: Stripe publishable key

## Agent Creation System (Automated)

### Automated Agent Creation Command (✅ FULLY FUNCTIONAL)
The project features a sophisticated automated agent creation system via the `create_agent` management command with complete Django template generation:

```bash
# Create webhook-based agent (N8N integration)
python manage.py create_agent "Agent Name" "agent-slug" webhook \
  --category utilities --price 2.5 \
  --webhook-url "https://webhook.url" --agent-id "123"

# Create API-based agent (Direct API integration)
python manage.py create_agent "Weather Reporter" "weather-reporter" api \
  --category utilities --price 2.5 \
  --api-base-url "https://api.openweathermap.org/data/2.5/weather" \
  --api-key-env "OPENWEATHER_API_KEY" --auth-method query
```

### Agent Creation System Architecture

#### Core Framework (agent_base app)
- **BaseAgent Model**: Database catalog for agent marketplace
- **BaseAgentRequest/BaseAgentResponse**: Abstract models for tracking requests
- **StandardWebhookProcessor**: Handles N8N webhook integrations with message payload format
- **StandardAPIProcessor**: Handles direct API calls with flexible authentication methods
- **WebhookFormatDetector**: Utility to test and detect webhook formats

#### Template-Based Code Generation (✅ COMPLETE)
The system uses Django templates in `agent_base/templates/agent_generator/` to generate complete agent apps:

**Available Template Files:**
- `api_models.py` / `webhook_models.py`: Database models with custom fields
- `api_processor.py` / `webhook_processor.py` / `weather_api_processor.py`: Processor classes
- `views.py`: Django views with authentication and wallet integration
- `urls.py`: URL routing patterns with proper namespacing
- `admin.py`: Django admin configuration
- `apps.py`: Django app configuration
- `__init__.py`: App initialization

#### Supported Agent Types

**1. Webhook Agents (N8N Integration)**
- Uses `StandardWebhookProcessor` base class
- Message-based payload format: `{'message': {'text': 'content'}, 'sessionId': '...', 'userId': '...', 'agentId': '...'}`
- Automatic error handling and retry logic
- Processing time tracking

**2. API Agents (Direct Integration)**
- Uses `StandardAPIProcessor` base class
- Multiple authentication methods: bearer, api-key, basic, query
- GET/POST request support
- Response parsing and formatting

#### Example Agents (Production Ready)

All agents now feature consistent architecture with standardized themes, unified CSS, and isolated JavaScript utilities for container-like functionality.

**Data Analysis Agent** (Price: 5.00 AED):
- **N8N Integration**: PDF analysis webhook processor
- **File Upload**: PDF, CSV, Excel files with drag-and-drop interface
- **Real-time Results**: AJAX display with wallet balance updates
- **Features**: Summary/Detailed/Statistical analysis types
- **Form Submission Pattern**: Uses unified form submission (not button click)
- **Unified CSS**: Uses agent-base.css with professional theme
- **Text Display**: Simple text formatting (no complex markdown parsing)
- **Architecture**: Standard agent-container grid layout (1fr 350px) with proper wallet positioning
- **JavaScript Isolation**: DataAnalyzerUtils with agent-specific functionality

**Weather Reporter Agent** (Price: 2.00 AED):
- **API Integration**: OpenWeatherMap API with direct calls
- **Custom Fields**: location, report_type, temperature, humidity, wind_speed
- **Formatted Reports**: Both current and detailed weather reports
- **Real-time Results**: Dynamic display below form
- **Error Handling**: API failures and invalid locations
- **Unified CSS**: Uses agent-base.css with professional theme
- **Architecture**: Standard agent-container grid layout with proper structure
- **JavaScript Isolation**: WeatherUtils with agent-specific functionality

**Social Ads Generator Agent** (Price: 7.00 AED):
- **N8N Integration**: Social media ad generation via webhook
- **Platform Support**: Facebook, Instagram, LinkedIn, Twitter/X, TikTok, YouTube
- **Multi-language**: English, Arabic, Spanish, French, German, Chinese
- **Real-time Results**: Dynamic content generation and display
- **Unified CSS**: Uses agent-base.css with creative theme (glassmorphism)
- **Architecture**: Standard agent-container grid layout with glassmorphism styling
- **JavaScript Isolation**: SocialAdsUtils with agent-specific functionality

**Job Posting Generator Agent** (Price: 4.00 AED):
- **N8N Integration**: Professional job posting creation
- **Comprehensive Forms**: Job details, requirements, company info
- **Multi-language Support**: Multiple output languages
- **Enhanced UX**: Progressive form validation and real-time feedback
- **Unified CSS**: Uses agent-base.css with professional theme
- **Architecture**: Standard agent-container grid layout with professional styling
- **JavaScript Isolation**: JobPostingUtils with agent-specific functionality

**Five Whys Analysis Agent** (Price: 3.00 AED):
- **N8N Integration**: Problem analysis using Five Whys methodology
- **Comprehensive UX**: Enhanced UI with styled cards and professional layout
- **Multi-language Support**: Multiple output languages
- **Real-time Results**: Dynamic analysis generation and display
- **Unified CSS**: Uses agent-base.css with professional theme
- **Architecture**: Standard agent-container grid layout with consistent styling
- **JavaScript Isolation**: FiveWhysUtils with agent-specific functionality

### Management Commands

#### create_agent (✅ READY TO USE)
Generates complete agent apps with:
- Database models and migrations
- Processor classes (API/webhook/weather-specific)
- Django views with authentication and wallet integration
- URL routing with proper namespacing
- Admin interface with list views
- Custom field definitions based on agent type
- Simplified template structure: `agent_name/templates/detail.html`

```bash
python manage.py create_agent --help

# Examples:
python manage.py create_agent "PDF Analyzer" "pdf-analyzer" api --price 5.0
python manage.py create_agent "Social Media Generator" "social-generator" webhook --price 3.0
```

#### test_webhook
Tests webhook endpoints to determine compatible formats:
```bash
# Test all formats
python manage.py test_webhook https://webhook.url

# Detect best format only
python manage.py test_webhook https://webhook.url --detect-best
```

### Manual Agent Creation (Legacy)

For custom agents requiring manual setup:

#### Step 1: Create Django App
```bash
python manage.py startapp agent_[name]
```

#### Step 2: Define Models
Extend `BaseAgentRequest` and `BaseAgentResponse` in `models.py`:
```python
from agent_base.models import BaseAgentRequest, BaseAgentResponse

class MyAgentRequest(BaseAgentRequest):
    # Add agent-specific fields
    input_text = models.TextField()

class MyAgentResponse(BaseAgentResponse):
    request = models.OneToOneField(MyAgentRequest, on_delete=models.CASCADE, related_name='response')
    output_text = models.TextField(blank=True)
```

#### Step 3: Create Processor
Choose between webhook or API processor:

**Webhook Processor:**
```python
from agent_base.processors import StandardWebhookProcessor

class MyAgentProcessor(StandardWebhookProcessor):
    agent_slug = 'my-agent'
    webhook_url = settings.N8N_WEBHOOK_MY_AGENT
    agent_id = '123'
    
    def prepare_message_text(self, **kwargs):
        return f"Process: {kwargs.get('input_text')}"
```

**API Processor:**
```python
from agent_base.processors import StandardAPIProcessor

class MyAgentProcessor(StandardAPIProcessor):
    agent_slug = 'my-agent'
    api_base_url = 'https://api.example.com/v1/process'
    api_key_env = 'MY_API_KEY'
    auth_method = 'bearer'
    
    def prepare_request_data(self, **kwargs):
        return {'text': kwargs.get('input_text')}
```

#### Step 4: Add to Configuration
- Add app to `INSTALLED_APPS` in `settings.py`
- Add URL routing in `netcop_hub/urls.py`
- Run migrations: `python manage.py makemigrations && python manage.py migrate`
- Create BaseAgent entry in database

## Database Models Relationships

### Core Models
- `User` (authentication): Custom user with wallet functionality
- `BaseAgent` (agent_base): Agent catalog/marketplace entries
- `WalletTransaction` (wallet): Payment and usage tracking

### Agent-Specific Models
Each agent app has:
- `[Agent]Request`: Inherits from `BaseAgentRequest`, tracks user requests
- `[Agent]Response`: Inherits from `BaseAgentResponse`, stores AI responses

### Key Relationships
- `User` 1:N `BaseAgentRequest` (user can make multiple requests)
- `BaseAgent` 1:N `BaseAgentRequest` (agent can have multiple requests)
- `BaseAgentRequest` 1:1 `BaseAgentResponse` (each request has one response)
- `User` 1:N `WalletTransaction` (user has transaction history)

## URL Structure

```
/                           # Homepage (core app)
/auth/login/               # Authentication
/auth/register/            # User registration
/agents/[agent-slug]/      # Individual agent pages
/admin/                    # Django admin
```

## Template Organization

Templates follow clean Django app structure:
- `templates/core/`: Homepage, marketplace, wallet (global templates)
- `templates/authentication/`: Login, registration (global templates)
- `[agent_name]/templates/[agent_name]/`: Individual agent templates within their respective apps (namespaced)
- `docs/`: All documentation and guides
- `tests/`: All test files

## Common Development Patterns

### Adding New Agent Fields
1. Add fields to agent request/response models
2. Update processor's `prepare_request_data()` method
3. Modify view's `process_request()` method
4. Update templates to include new fields

### Debugging Webhook Issues
1. Check webhook URL in `.env` file
2. Examine processor logs in console output
3. Verify JSON payload format in `prepare_request_data()`
4. Test webhook independently with tools like Postman

### Managing Agent Pricing
1. Update price in `populate_base_agents.py`
2. Run `python manage.py populate_base_agents` to update database
3. Pricing is enforced in `BaseAgentView.post()` method

## 💰 Wallet Management Best Practices (CRITICAL)

### ✅ CORRECT Wallet Deduction Pattern
**ALWAYS deduct wallet balance ONLY after successful processing, not before!**

#### View Layer (NO wallet deduction):
```python
# ❌ NEVER do this in views.py:
# request.user.deduct_balance(agent.price, description, agent_slug)

# ✅ CORRECT: Only check balance, create request object
if not request.user.has_sufficient_balance(agent.price):
    return JsonResponse({'error': 'Insufficient wallet balance'}, status=400)

agent_request = MyAgentRequest.objects.create(
    user=request.user,
    agent=agent,
    cost=agent.price,
    # ... other fields
)

# Process request via processor
processor = MyAgentProcessor()
result = processor.process_request(request_obj=agent_request, ...)

# Return response with updated wallet balance
request.user.refresh_from_db()
return JsonResponse({
    'success': True,
    'request_id': str(agent_request.id),
    'wallet_balance': float(request.user.wallet_balance)  # Real-time balance
})
```

#### Processor Layer (wallet deduction after success):
```python
def process_response(self, response_data, request_obj):
    try:
        # ... process response and determine success
        success = response_data.get('status') == 'success' and bool(analysis_text)
        
        # Create response object
        response_obj = MyAgentResponse.objects.create(
            request=request_obj,
            success=success,
            # ... other fields
        )
        
        # ✅ ONLY deduct wallet after successful processing
        if success:
            request_obj.user.deduct_balance(
                request_obj.cost,
                f"Agent Name - {description}",
                'agent-slug'
            )
            print(f"Wallet deducted {request_obj.cost} AED for successful processing")
        
        request_obj.status = 'completed' if success else 'failed'
        request_obj.save()
        
        return response_obj
    except Exception as e:
        # ✅ On error: NO wallet deduction, request marked as failed
        request_obj.status = 'failed'
        request_obj.save()
        raise
```

#### Frontend JavaScript (real-time balance updates):
```javascript
// Update wallet balance after successful processing
if (result.success && result.status === 'completed') {
    // Update wallet balance display
    if (result.wallet_balance !== undefined) {
        updateWalletBalance(result.wallet_balance);
    }
    
    showToast('✅ Analysis completed and payment processed!', 'success');
} else if (result.status === 'failed') {
    showToast('❌ Analysis failed - no charge applied', 'error');
}

function updateWalletBalance(newBalance) {
    // Update all wallet displays in real-time
    document.querySelectorAll('[data-wallet-balance]').forEach(element => {
        element.textContent = `${newBalance.toFixed(2)} AED`;
    });
    window.currentWalletBalance = newBalance;
}
```

### 🔥 Critical Wallet Rules
1. **NEVER** deduct wallet in views.py before processing
2. **ALWAYS** deduct wallet in processor ONLY after `success=True`
3. **ALWAYS** return updated `wallet_balance` in JSON responses
4. **ALWAYS** update frontend wallet display in real-time
5. **ALWAYS** show clear user feedback: "payment processed" vs "no charge applied"

### Wallet Flow Summary
```
1. User uploads/submits → NO charge yet ✅
2. Create request object → NO charge yet ✅
3. Start processing → NO charge yet ✅
4. Processing succeeds → CHARGE NOW ✅
5. Update frontend → Show new balance ✅
6. If any step fails → NO charge at all ✅
```

This ensures users never lose money for failed processing while maintaining simple, efficient code.

## Payment System Architecture

### Stripe Integration (API-Based Verification)

The payment system uses **API-based verification** instead of webhooks for reliable, instant payment processing:

#### Payment Flow
```
1. User clicks "💳 Top Up Wallet"
2. Create Stripe checkout session via API
3. User completes payment on Stripe
4. Stripe redirects to success page with session_id
5. Success page verifies payment via Stripe API
6. Wallet balance updated immediately
7. Transaction recorded as "Wallet top-up via Stripe"
```

#### Key Components
- **StripePaymentHandler** (`wallet/stripe_handler.py`): Handles session creation and verification
- **Success Page Verification** (`core/views.py`): Automatic payment verification on return
- **Clean Transaction Descriptions**: Professional "Wallet top-up via Stripe" messages
- **No Webhook Dependency**: Reliable without webhook delivery issues

#### Configuration
```python
# settings.py
STRIPE_SECRET_KEY = 'sk_test_...'  # From .env
STRIPE_PUBLISHABLE_KEY = 'pk_test_...'  # From .env
STRIPE_WEBHOOK_SECRET = 'whsec_...'  # Optional (backup)
```

#### Environment Variables
```bash
# .env
STRIPE_SECRET_KEY=sk_test_your_key_here
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_secret_here  # Optional
```

### Payment System URLs
- `/wallet/` - Wallet overview and transactions
- `/wallet/topup/` - Payment amount selection
- `/wallet/top-up/success/` - Payment verification and confirmation
- `/wallet/top-up/cancel/` - Payment cancellation
- `/stripe/debug/` - Stripe connectivity debugging (dev only)

### Advantages of API Verification
- **Instant confirmation** - No waiting for webhook delivery
- **Reliable** - No webhook delivery failures
- **Immediate user feedback** - Balance updates immediately
- **Simpler debugging** - You control the verification timing
- **Production-proven** - Used by many successful platforms

## Unified CSS and UI System

### Agent Styling Architecture
All agents now use a unified CSS system for consistent user experience and maintainability:

#### Core Files
- **`/static/css/agent-base.css`**: Unified component library for all agents
- **`/static/css/themes.css`**: Global color variables and themes
- **Agent-specific JavaScript utilities**: Each agent has isolated JavaScript functions for container-like functionality

### Agent Isolation Architecture

#### Container-like Functionality
All agents now implement true isolation to prevent cross-agent interference:

**JavaScript Isolation Pattern:**
```javascript
// Each agent has its own utility namespace
const DataAnalyzerUtils = { /* agent-specific functions */ };
const WeatherUtils = { /* agent-specific functions */ };
const SocialAdsUtils = { /* agent-specific functions */ };
const JobPostingUtils = { /* agent-specific functions */ };
const FiveWhysUtils = { /* agent-specific functions */ };

// For backward compatibility, each agent creates AgentUtils alias
const AgentUtils = DataAnalyzerUtils; // or appropriate agent utils
```

**Benefits of Isolation:**
- No shared dependencies between agents
- Changes to one agent don't affect others
- Agent-specific functionality can be customized
- Easier debugging and maintenance
- Container-like isolation without containerization complexity

#### Theme System
The unified CSS supports multiple themes via CSS custom properties:

1. **Professional Theme** (Default - Black & White):
   - Used by: Job Posting Generator, Data Analyzer, Weather Reporter
   - Clean, corporate appearance with subtle shadows
   - Focused on readability and professional presentation

2. **Creative Theme** (Pink/Purple with Glassmorphism):
   - Used by: Social Ads Generator
   - Vibrant gradients and glassmorphism effects
   - Enhanced visual appeal for creative content

3. **Minimal Theme** (Light Gray):
   - Available for future agents requiring minimal design
   - Subtle styling with maximum content focus

#### Implementation Pattern
```html
<!-- Standard agent template structure -->
<div class="agent-page theme-professional">  <!-- or theme-creative, theme-minimal -->
    <div class="agent-container">
        <div>
            <!-- Main content area (first grid column) -->
            <div class="card">
                <h3 class="section-title">Agent Title</h3>
                <!-- Agent form and content -->
            </div>
            <!-- Processing status and results stay within first grid column -->
        </div>
        <div class="wallet-section">
            <!-- Wallet sidebar (second grid column) -->
            <div class="card">
                <h3 class="section-title">💳 Your Wallet</h3>
                <!-- Wallet content -->
            </div>
        </div>
    </div>
</div>
```

#### Standardized Layout Architecture

**Grid Layout System:**
- `agent-container`: CSS Grid with `grid-template-columns: 1fr 350px`
- **First column**: Main content, forms, processing status, results
- **Second column**: Wallet sidebar (350px width)
- **Mobile responsive**: Single column on screens < 768px

**Critical Structure Rules:**
1. **Wallet positioning**: `wallet-section` must be a direct child of `agent-container` (separate grid column)
2. **Content hierarchy**: All agent content stays in first grid column
3. **Processing status**: Displays below form, spans full width of first column
4. **Results display**: Shows below processing status in first column

**Data Analyzer Wallet Fix Example:**
```html
<!-- ❌ INCORRECT: wallet-section inside main content -->
<div class="agent-container">
    <div>
        <form>...</form>
        <div class="wallet-section">...</div>  <!-- Wrong placement -->
    </div>
</div>

<!-- ✅ CORRECT: wallet-section as separate grid column -->
<div class="agent-container">
    <div>
        <form>...</form>
        <!-- Processing Status -->
        <!-- Results -->
    </div>
    <div class="wallet-section">...</div>  <!-- Correct placement -->
</div>
```

### Text Display Standardization

#### Simple Text Formatting Approach
After testing complex markdown parsing, the system now uses simplified text formatting for better reliability:

**Current Implementation:**
```javascript
// Simple text formatting in AgentUtils.parseMarkdown()
parseMarkdown(text) {
    if (!text) return '';
    return text
        .replace(/\*\*/g, '') // Remove markdown bold syntax
        .replace(/\#{1,3}\s/g, '') // Remove header syntax
        .replace(/\n{3,}/g, '\n\n') // Reduce excessive line breaks
        .replace(/\n/g, '<br>') // Convert line breaks to HTML
        .trim();
}
```

**Benefits:**
- No external dependencies (removed Marked.js + DOMPurify)
- Consistent formatting across all agents
- No risk of layout breaking from complex markdown
- Fast rendering and simple maintenance

#### CSS Text Styling
```css
.results-content {
    line-height: 1.6;
    word-wrap: break-word;
    overflow-wrap: break-word;
    white-space: pre-line; /* Preserves line breaks */
}
```

### Form Submission Standardization

All agents now use consistent form submission patterns:

#### Unified Pattern
```javascript
// Standard form submission handler
document.getElementById('agentForm').addEventListener('submit', function(e) {
    e.preventDefault();
    
    // Validation, authentication, and balance checks
    if (!isFormValid()) return;
    
    // Submit via FormData with CSRF token (automatic inclusion)
    const formData = new FormData(this);
    
    fetch(window.location.href, {
        method: 'POST',
        body: formData,
        headers: { 'X-Requested-With': 'XMLHttpRequest' }
    })
    .then(response => response.json())
    .then(result => {
        // Handle polling or immediate response
        if (result.success && result.request_id) {
            pollForResults(result.request_id);
        } else {
            displayResults(result);
        }
    });
});
```

#### Key Improvements
- **Form submission** instead of button click handlers
- **Automatic CSRF handling** via FormData(form)
- **Consistent error handling** across all agents
- **Unified polling mechanism** for webhook-based agents

## Current Architecture (Clean & Modern)

The project uses a clean, modular individual agent architecture:

### Current System Features
- **Individual agent apps**: Each agent is a separate Django app (`weather_reporter/`, etc.)
- **Clean template organization**: Templates live within their respective agent apps
- **Organized project structure**: Documentation in `docs/`, tests in `tests/`, clean root directory
- **BaseAgent catalog system**: Centralized marketplace with individual agent implementations
- **Modular processors**: Each agent has its own processor for API/webhook integration
- **App-specific templates**: `agent_name/templates/agent_name/detail.html` (namespaced to prevent conflicts)

### Best Practices

#### Agent Development Standards
- **Individual App Architecture**: Each agent is a separate Django app
- **Template Organization**: Place templates within agent app (`agent_name/templates/agent_name/`)
- **Automated Creation**: Use `create_agent` command for initial setup
- **Clean Structure**: Keep root directory organized with `docs/` and `tests/` folders

#### Modern Agent Features (Required)
- **Real-time Results Display**: Use AJAX to show results below form without page reload
- **Wallet Balance Updates**: Update balance displays immediately after successful processing
- **Data Attributes**: Add `data-wallet-balance` to all balance elements for easy targeting
- **Continuous Workflow**: Allow multiple requests without page refresh ("Get Another" functionality)
- **Clear User Feedback**: Show "payment processed" vs "no charge applied" messages
- **Standardized Layout**: Use agent-container grid layout (1fr 350px) with proper wallet positioning
- **Theme Consistency**: Apply unified CSS themes across all agents
- **JavaScript Isolation**: Agent-specific utilities for container-like functionality

#### Recent Standardization Improvements (2024)

**Agent Architecture Consistency:**
All 5 production agents now follow standardized patterns:
1. **Data Analyzer**: Reduced custom CSS from 400+ lines to ~78 lines, standardized HTML structure
2. **Job Posting Generator**: Enhanced with professional theme and proper grid layout
3. **Five Whys Analyzer**: Applied black and white theme with consistent styling
4. **Social Ads Generator**: Maintained creative theme while standardizing structure
5. **Weather Reporter**: Professional theme with clean weather data presentation

**Key Improvements Made:**
- **HTML Structure**: All agents use standard `agent-container` grid layout
- **CSS Consolidation**: Removed duplicate styles, standardized on `agent-base.css`
- **Wallet Positioning**: Fixed wallet appearing at bottom vs. right side across all agents
- **JavaScript Isolation**: Each agent has isolated utilities (DataAnalyzerUtils, WeatherUtils, etc.)
- **Theme Application**: Consistent theme implementation across all agents
- **Code Reduction**: Eliminated 400+ lines of redundant CSS code

#### Frontend JavaScript Requirements
```javascript
// Required functions for all agents:
- updateWalletBalance(newBalance)  // Updates all balance displays
- displayResults(result)          // Shows results below form  
- pollForResults(requestId)       // Checks processing status
- resetForm()                     // Prepares for next request
```

#### CSRF Token Requirements
All agent templates that use JavaScript form submission must include:
```html
<!-- Required: Add CSRF token to template -->
{% csrf_token %}
```

For manual FormData submission (like data analyzer), access token via:
```javascript
// For templates with {% csrf_token %} tag
formData.append('csrfmiddlewaretoken', document.querySelector('[name=csrfmiddlewaretoken]').value);

// For HTML forms with {% csrf_token %} inside form
const formData = new FormData(this); // 'this' refers to form element - automatically includes CSRF
```

#### Template Requirements
```html
<!-- Required data attributes for wallet balance -->
<span data-wallet-balance>{{ user.wallet_balance|floatformat:2 }} AED</span>
<div data-wallet-balance>{{ user.wallet_balance|floatformat:2 }} AED</div>
```

## 🔐 Password Reset System (Implemented July 2024)

### Overview
A comprehensive forgot password system has been implemented with secure token-based authentication, professional UI, and Railway deployment support.

### Key Features
- **Secure Token System**: UUID-based tokens with 1-hour expiration
- **Email Integration**: Gmail SMTP with production-ready configuration
- **Professional UI**: Responsive design matching existing authentication pages
- **Railway Deployment**: Automatic environment detection and proper URL generation
- **User Experience**: Clear error messages and helpful navigation
- **Security**: Single-use tokens, no email enumeration, comprehensive logging

### Database Schema
```python
class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_reset_tokens')
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    
    def is_valid(self):
        return not self.is_used and timezone.now() < self.expires_at
    
    def mark_as_used(self):
        self.is_used = True
        self.save()
```

### URL Configuration
```python
# authentication/urls.py
urlpatterns = [
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/<uuid:token>/', views.reset_password_view, name='reset_password'),
]
```

### User Experience Flow
1. **Request Reset**: User clicks "Forgot your password?" on login page
2. **Email Validation**: System shows helpful error if user doesn't exist
3. **Token Generation**: Secure UUID token created with 1-hour expiration
4. **Email Delivery**: Professional email sent with reset instructions
5. **Password Reset**: User clicks link, enters new password
6. **Completion**: Token marked as used, user redirected to login

### Railway Deployment Configuration
```python
# Automatic environment detection
if config('RAILWAY_ENVIRONMENT', default=''):
    SITE_URL = 'https://netcop.up.railway.app'
else:
    SITE_URL = config('SITE_URL', default='http://localhost:8000')
```

### Required Environment Variables (Railway)
```bash
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
DEFAULT_FROM_EMAIL=NetCop <your-email@gmail.com>
```

### Security Features
- **Token Expiration**: All tokens expire after 1 hour
- **Single-Use**: Tokens are marked as used after password reset
- **No Email Enumeration**: Helpful error messages without revealing account existence
- **Secure URLs**: HTTPS links in production environment
- **Logging**: Comprehensive error logging for debugging

### Error Handling
- **Clear Messages**: "No account found with email X. Please check your email or create account"
- **Helpful Navigation**: Direct links to registration page
- **Email Failures**: Detailed error messages for debugging
- **Token Validation**: Proper handling of expired/invalid tokens

### Testing
```bash
# Test email configuration
python manage.py test_email --email=user@example.com

# Manual testing flow
1. Go to /auth/forgot-password/
2. Enter registered user email
3. Check email inbox (including spam)
4. Click reset link
5. Set new password
6. Login with new credentials
```

### Files Created/Modified
- `authentication/models.py` - Added PasswordResetToken model
- `authentication/views.py` - Added forgot_password_view and reset_password_view
- `authentication/urls.py` - Added password reset URL patterns
- `templates/authentication/forgot_password.html` - Professional forgot password form
- `templates/authentication/reset_password.html` - Password reset form
- `templates/authentication/login.html` - Added forgot password link
- `netcop_hub/settings.py` - Email and site URL configuration
- `authentication/management/commands/test_email.py` - Email testing utility
- `docs/FORGOT_PASSWORD_IMPLEMENTATION.md` - Comprehensive documentation

### Common Issues & Solutions
1. **Email not received**: Check spam folder, verify Railway environment variables
2. **Link not working**: Ensure SITE_URL is correctly configured for Railway
3. **Token expired**: Tokens expire after 1 hour, request new reset
4. **User not found**: Register user first, then request password reset

### Implementation Notes
- The system uses Django's built-in password validation
- Email templates are plain text for maximum compatibility
- Token cleanup can be implemented via periodic task if needed
- System is production-ready and deployed on Railway

This implementation provides a secure, user-friendly password reset system that integrates seamlessly with the existing NetCop authentication flow.