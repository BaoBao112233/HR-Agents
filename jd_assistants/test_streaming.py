"""
Quick test script for streaming agents
"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

from jd_assistants.inference.groq import ChatGroq
from jd_assistants.agent.jd_rewriter import JDRewriterAgent

# Sample JD text for testing
SAMPLE_JD = """
Software Engineer

We need someone to write code. Must know Python.
Experience: 2 years
Salary: Negotiable
"""


async def test_streaming_analyze():
    """Test streaming JD analysis"""
    print("=" * 80)
    print("Testing Streaming JD Analysis")
    print("=" * 80)
    
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=api_key, temperature=0)
    agent = JDRewriterAgent(llm)
    
    print("\n📝 Original JD:")
    print(SAMPLE_JD)
    print("\n🤔 AI Thinking Process (streaming):")
    print("-" * 80)
    
    async for chunk in agent.astream_analyze_jd(SAMPLE_JD):
        if chunk.get("type") == "progress":
            # Print thinking progress
            print(chunk.get("content", ""), end="", flush=True)
        elif chunk.get("type") == "final":
            print("\n" + "-" * 80)
            print("\n✅ Final Analysis:")
            data = chunk.get("data")
            if data:
                print(f"\n🎯 Thinking: {data.thinking}")
                print(f"\n📊 Overall Score: {data.overall_score}/100")
                print(f"\n💡 Key Recommendations:")
                for rec in data.key_recommendations:
                    print(f"  - {rec}")
                print(f"\n🔧 Improvements ({len(data.improvements)}):")
                for imp in data.improvements[:3]:  # Show first 3
                    print(f"  • {imp.section}: {imp.reason}")
        elif chunk.get("type") == "error":
            print(f"\n❌ Error: {chunk.get('error')}")


async def test_streaming_rewrite():
    """Test streaming JD rewrite"""
    print("\n\n" + "=" * 80)
    print("Testing Streaming JD Rewrite")
    print("=" * 80)
    
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=api_key, temperature=0)
    agent = JDRewriterAgent(llm)
    
    print("\n📝 Original JD:")
    print(SAMPLE_JD)
    print("\n🤔 AI Thinking Process (streaming):")
    print("-" * 80)
    
    async for chunk in agent.astream_rewrite_jd(SAMPLE_JD):
        if chunk.get("type") == "progress":
            print(chunk.get("content", ""), end="", flush=True)
        elif chunk.get("type") == "final":
            print("\n" + "-" * 80)
            print("\n✅ Final Rewrite:")
            data = chunk.get("data")
            if data:
                print(f"\n🎯 Thinking: {data.thinking}")
                print(f"\n✨ Rewritten JD:")
                print(data.rewritten_jd)
                print(f"\n🔄 Key Changes:")
                for change in data.key_changes:
                    print(f"  - {change}")
        elif chunk.get("type") == "error":
            print(f"\n❌ Error: {chunk.get('error')}")


async def test_structured_output():
    """Test non-streaming structured output"""
    print("\n\n" + "=" * 80)
    print("Testing Structured Output (Non-Streaming)")
    print("=" * 80)
    
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model='llama-3.3-70b-versatile', api_key=api_key, temperature=0)
    agent = JDRewriterAgent(llm)
    
    print("\n📝 Original JD:")
    print(SAMPLE_JD)
    print("\n⏳ Analyzing (non-streaming)...")
    
    result = agent.analyze_jd_structured(SAMPLE_JD)
    
    print(f"\n✅ Analysis Complete!")
    print(f"\n🎯 Thinking: {result.thinking}")
    print(f"📊 Overall Score: {result.overall_score}/100")
    print(f"💡 Recommendations: {len(result.key_recommendations)}")
    print(f"🔧 Improvements: {len(result.improvements)}")


async def main():
    """Run all tests"""
    print("\n🚀 Starting Agent Streaming Tests\n")
    
    # Test 1: Streaming analyze
    await test_streaming_analyze()
    
    # Test 2: Streaming rewrite
    await test_streaming_rewrite()
    
    # Test 3: Structured output (non-streaming)
    await test_structured_output()
    
    print("\n\n✅ All tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
