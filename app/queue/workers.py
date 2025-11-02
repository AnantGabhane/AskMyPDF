from ..db.collections.file import files_collection
from bson import ObjectId
import os
from pdf2image import convert_from_path
import google.generativeai as genai
from PIL import Image
from typing import List
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from environment
api_key = os.getenv("GOOGLE_API_KEY")

# Validate API key exists
if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found in environment variables. "
        "Please add it to your .env file."
    )

# ⭐ CRITICAL: Configure Gemini with the API key
genai.configure(api_key=api_key)

print(f"✅ Gemini API configured successfully")


async def process_file(id: str, file_path: str):
    """Process PDF file using Gemini Vision API"""
    
    try:
        # Update status: processing
        await files_collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": {"status": "processing"}}
        )
        
        # Update status: converting to images
        await files_collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": {"status": "converting to images"}}
        )
        
        # Step 1: Convert the PDF to images
        pages = convert_from_path(file_path)
        images = []
        
        for i, page in enumerate(pages):
            image_save_path = f"/mnt/uploads/images/{id}/image-{i}.jpg"
            os.makedirs(os.path.dirname(image_save_path), exist_ok=True)
            page.save(image_save_path, 'JPEG')
            images.append(image_save_path)
        
        # Update status: conversion success
        await files_collection.update_one(
            {"_id": ObjectId(id)}, 
            {
                "$set": {
                    "status": "converting to images success",
                    "total_pages": len(images)
                }
            }
        )
        
        # Step 2: Process with Gemini Vision API
        await files_collection.update_one(
            {"_id": ObjectId(id)}, 
            {"$set": {"status": "analyzing with AI"}}
        )
        
        # Initialize Gemini model
        model = genai.GenerativeModel('models/gemini-robotics-er-1.5-preview')
        
        # Prepare content for Gemini
        content_parts = ["Based on the resume below, Roast this resume\n\n"]
        
        # Add all pages (Gemini can handle multiple images)
        for img_path in images:
            img = Image.open(img_path)
            content_parts.append(img)
        
        # Generate content with all images
        response = model.generate_content(content_parts)
        
        # Extract result text
        result_text = response.text
        
        # Update status: processed
        await files_collection.update_one(
            {"_id": ObjectId(id)}, 
            {
                "$set": {
                    "status": "processed",
                    "result": result_text,
                    "processed_pages": len(images)
                }
            }
        )
        
        print(f"✅ Successfully processed file {id}")
        return result_text
        
    except Exception as e:
        print(f"❌ Error processing file {id}: {str(e)}")
        # Update status: failed
        await files_collection.update_one(
            {"_id": ObjectId(id)}, 
            {
                "$set": {
                    "status": "failed",
                    "error": str(e)
                }
            }
        )
        raise e