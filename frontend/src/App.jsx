import { useState, useEffect, useRef } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Separator } from '@/components/ui/separator.jsx'
import { Send, MessageCircle, History, BookOpen, Loader2 } from 'lucide-react'
import './App.css'

// Define the backend API URL
const API_BASE_URL = 'http://localhost:5000'; // This should point to your Flask backend

function App() {
  const [messages, setMessages] = useState([])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionId, setSessionId] = useState('')
  const [currentLanguage, setCurrentLanguage] = useState('en')
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  useEffect(() => {
    // Generate a new session ID when the app starts
    setSessionId(generateSessionId())
    
    // Add welcome message
    setMessages([{
      role: 'assistant',
      content: 'Welcome! I am the Chronicler of the Nile, your guide through the vast tapestry of Egyptian history. From the ancient pharaohs to modern times, I am here to share the stories, events, and wisdom of this extraordinary land. What period or aspect of Egyptian history would you like to explore?\n\nمرحباً! أنا راوي النيل، دليلك عبر تاريخ مصر العريق. من الفراعنة القدماء إلى العصر الحديث، أنا هنا لأشاركك القصص والأحداث وحكمة هذه الأرض العظيمة. أي فترة أو جانب من التاريخ المصري تود استكشافه؟',
      timestamp: new Date().toISOString(),
      language: 'en'
    }])
  }, [])

  const generateSessionId = () => {
    return 'session_' + Math.random().toString(36).substr(2, 9) + '_' + Date.now()
  }

  const detectLanguage = (text) => {
    // Simple Arabic detection
    const arabicPattern = /[\u0600-\u06FF]/
    return arabicPattern.test(text) ? 'ar' : 'en'
  }

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage = {
      role: 'user',
      content: inputMessage,
      timestamp: new Date().toISOString(),
      language: detectLanguage(inputMessage)
    }

    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await fetch(`${API_BASE_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputMessage,
          session_id: sessionId
        })
      })

      if (!response.ok) {
        throw new Error('Failed to send message')
      }

      const data = await response.json()
      
      const aiMessage = {
        role: 'assistant',
        content: data.response,
        timestamp: data.timestamp,
        language: data.language
      }

      setMessages(prev => [...prev, aiMessage])
      setCurrentLanguage(data.language)
      
    } catch (error) {
      console.error('Error sending message:', error)
      const errorMessage = {
        role: 'assistant',
        content: 'I apologize, but I encountered an error. Please try again. / أعتذر، لكنني واجهت خطأ. يرجى المحاولة مرة أخرى.',
        timestamp: new Date().toISOString(),
        language: 'en'
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp).toLocaleTimeString([], { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-amber-50 via-orange-50 to-yellow-50 dark:from-amber-950 dark:via-orange-950 dark:to-yellow-950">
      {/* Header */}
      <div className="border-b bg-white/80 dark:bg-gray-900/80 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-gradient-to-br from-amber-500 to-orange-600 rounded-lg flex items-center justify-center">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  The Chronicler of the Nile
                </h1>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  راوي النيل - Your Egyptian History AI Guide
                </p>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <Badge variant="secondary" className="text-xs">
                <MessageCircle className="w-3 h-3 mr-1" />
                Session Active
              </Badge>
              <Badge variant="outline" className="text-xs">
                {currentLanguage === 'ar' ? 'العربية' : 'English'}
              </Badge>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="container mx-auto px-4 py-6 max-w-4xl">
        <Card className="h-[calc(100vh-200px)] flex flex-col bg-white/90 dark:bg-gray-900/90 backdrop-blur-sm border-amber-200 dark:border-amber-800">
          <CardHeader className="pb-4">
            <CardTitle className="flex items-center text-lg">
              <History className="w-5 h-5 mr-2 text-amber-600" />
              Conversation with the Chronicler
            </CardTitle>
          </CardHeader>
          
          <CardContent className="flex-1 flex flex-col p-0">
            {/* Messages Area */}
            <ScrollArea className="flex-1 px-6">
              <div className="space-y-4 pb-4">
                {messages.map((message, index) => (
                  <div
                    key={index}
                    className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[80%] rounded-lg px-4 py-3 ${
                        message.role === 'user'
                          ? 'bg-amber-500 text-white'
                          : 'bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-white border border-amber-200 dark:border-amber-800'
                      }`}
                    >
                      <div className="whitespace-pre-wrap text-sm leading-relaxed">
                        {message.content}
                      </div>
                      <div className={`text-xs mt-2 opacity-70 ${
                        message.role === 'user' ? 'text-amber-100' : 'text-gray-500 dark:text-gray-400'
                      }`}>
                        {formatTimestamp(message.timestamp)}
                      </div>
                    </div>
                  </div>
                ))}
                
                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-gray-100 dark:bg-gray-800 rounded-lg px-4 py-3 border border-amber-200 dark:border-amber-800">
                      <div className="flex items-center space-x-2">
                        <Loader2 className="w-4 h-4 animate-spin text-amber-600" />
                        <span className="text-sm text-gray-600 dark:text-gray-400">
                          The Chronicler is thinking...
                        </span>
                      </div>
                    </div>
                  </div>
                )}
                
                <div ref={messagesEndRef} />
              </div>
            </ScrollArea>

            <Separator className="bg-amber-200 dark:bg-amber-800" />

            {/* Input Area */}
            <div className="p-6">
              <div className="flex space-x-2">
                <Input
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Ask about any period in Egyptian history... / اسأل عن أي فترة في التاريخ المصري..."
                  className="flex-1 border-amber-200 dark:border-amber-800 focus:border-amber-500 dark:focus:border-amber-500"
                  disabled={isLoading}
                />
                <Button
                  onClick={sendMessage}
                  disabled={!inputMessage.trim() || isLoading}
                  className="bg-amber-500 hover:bg-amber-600 text-white"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
              
              <div className="mt-3 text-xs text-gray-500 dark:text-gray-400 text-center">
                Explore Ancient Egypt • Graeco-Roman Period • Islamic Era • Ottoman Rule • Modern Egypt
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}

export default App



