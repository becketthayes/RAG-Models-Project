import React from 'react';
import { Box, Typography, Button } from '@mui/material';
import AddCircleOutlineIcon from '@mui/icons-material/AddCircleOutline';

const CreateNewRAGModel =  ({ onModelCreate }) => (
    <Box sx={{ border: '1px solid #e0e0e0', borderRadius: '8px', p: 2, bgcolor: 'white', maxWidth: '1000px', width: '100%', mt: 15 }}>
        <Box sx={{ border: '4px dashed #e0e0e0', borderRadius: '8px', p: 4, textAlign: 'center' }}>
            <AddCircleOutlineIcon sx={{ fontSize: 48, color: '#4CAF50'}} />
            <Typography variant='h3' sx={{ mt: 2 }}>
                Create a New RAG Model
            </Typography>
            <Typography variant='h5' sx={{ mt: 1, color: 'text.secondary' }}>
                Start a new project by defining your data sources and model parameters
            </Typography>

            <Button
                variant="contained"
                sx = {{
                    mt: 6,
                    bgcolor: '#4CAF50',
                    color: 'black',
                    fontSize: 20,
                    borderRadius: 6,
                    maxWidth: '300px', width: '100%',
                    '&:hover': { bgcolor: '#45a049' }
                }}
                onClick={onModelCreate}
            >
                Create New Model
            </Button>
        </Box>
    </Box>
    
);

export default CreateNewRAGModel