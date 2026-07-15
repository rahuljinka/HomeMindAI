import React from 'react';
import { View, ActivityIndicator } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { MessageSquare, Package, Home as HomeIcon } from 'lucide-react-native';
import { useAuthStore } from '../store/authStore';

import LoginScreen from '../screens/LoginScreen';
import RegisterScreen from '../screens/RegisterScreen';
import ChatScreen from '../screens/ChatScreen';
import ObjectsScreen from '../screens/ObjectsScreen';
import RoomsScreen from '../screens/RoomsScreen';
import HousesScreen from '../screens/HousesScreen';

const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

function RoomsStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen 
        name="Houses" 
        component={HousesScreen} 
        options={{ headerShown: false }} 
      />
      <Stack.Screen 
        name="Rooms" 
        component={RoomsScreen} 
        options={{ headerShown: false }} 
      />
    </Stack.Navigator>
  );
}

function MainTabs() {
  return (
    <Tab.Navigator
      detachInactiveScreens={false}
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: '#999',
        headerShown: false, // Changed to false because RoomsScreen has its own header now
      }}
    >
      <Tab.Screen 
        name="ChatTab" 
        component={ChatScreen} 
        options={{ 
          title: 'Chat',
          tabBarIcon: (props) => <MessageSquare size={props.size} color={props.color} />,
          headerTitle: 'HomeMind AI',
          headerShown: true,
        }} 
      />
      <Tab.Screen 
        name="ObjectsTab" 
        component={ObjectsScreen} 
        options={{ 
          title: 'Objects',
          tabBarIcon: (props) => <Package size={props.size} color={props.color} />,
          headerTitle: 'My Objects',
          headerShown: true,
        }} 
      />
      <Tab.Screen 
        name="RoomsTab" 
        component={RoomsStack} 
        options={{ 
          title: 'Houses',
          tabBarIcon: (props) => <HomeIcon size={props.size} color={props.color} />,
          headerShown: false,
        }} 
      />
    </Tab.Navigator>
  );
}

export default function AppNavigator() {
  const { isAuthenticated, isHydrated } = useAuthStore();

  if (!isHydrated) {
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#007AFF" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator detachInactiveScreens={false}>
        {!isAuthenticated ? (
          <>
            <Stack.Screen name="Login" component={LoginScreen} options={{ headerShown: false }} />
            <Stack.Screen name="Register" component={RegisterScreen} options={{ headerShown: true }} />
          </>
        ) : (
          <Stack.Screen name="Main" component={MainTabs} options={{ headerShown: false }} />
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
