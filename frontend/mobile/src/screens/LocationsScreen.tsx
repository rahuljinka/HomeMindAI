import React, { useState, useEffect } from 'react';
import { View, Text, FlatList, StyleSheet, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { Home, ChevronRight, LogOut, Building2, Smartphone, Box, Package } from 'lucide-react-native';
import apiClient from '../api/client';
import { useAuthStore } from '../store/authStore';

interface Container {
  id: number;
  name: string;
}

interface Furniture {
  id: number;
  name: string;
  type?: string;
  containers: Container[];
}

interface Room {
  id: number;
  name: string;
  description?: string;
  furniture: Furniture[];
}

interface House {
  id: number;
  name: string;
  description?: string;
  rooms: Room[];
}

type ViewType = 'HOUSES' | 'ROOMS' | 'FURNITURE' | 'CONTAINERS' | 'OBJECTS';

interface Breadcrumb {
  type: ViewType;
  id: number;
  name: string;
  data?: any;
}

export default function LocationsScreen({ navigation, route }: any) {
  const [houses, setHouses] = useState<House[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [breadcrumbs, setBreadcrumbs] = useState<Breadcrumb[]>([]);
  const [currentItems, setCurrentItems] = useState<any[]>([]);
  const [viewType, setViewType] = useState<ViewType>('HOUSES');
  const [objects, setObjects] = useState<any[]>([]);

  const logout = useAuthStore(state => state.logout);

  useEffect(() => {
    if (route.params?.initialBreadcrumbs) {
      setBreadcrumbs(route.params.initialBreadcrumbs);
    }
  }, [route.params?.initialBreadcrumbs]);

  const fetchHouses = async () => {
    try {
      setLoading(true);
      const response = await apiClient.get('/locations/');
      setHouses(response.data);
      
      const targetBreadcrumbs = route.params?.initialBreadcrumbs || breadcrumbs;
      if (targetBreadcrumbs.length === 0) {
        setCurrentItems(response.data);
        setViewType('HOUSES');
      } else {
        updateCurrentItems(response.data, targetBreadcrumbs);
      }
    } catch (error) {
      console.error('Error fetching locations:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  const fetchObjects = async (locationParams: { roomId?: number, furnitureId?: number, containerId?: number }) => {
    try {
      setLoading(true);
      const response = await apiClient.get('/objects/');
      const { roomId, furnitureId, containerId } = locationParams;
      
      // Filter objects based on the deepest provided location level
      const filtered = response.data.filter((obj: any) => {
        const loc = obj.current_location;
        if (!loc) return false;

        if (containerId !== undefined) {
          return loc.container?.id === containerId;
        }
        if (furnitureId !== undefined) {
          return loc.furniture?.id === furnitureId && !loc.container;
        }
        if (roomId !== undefined) {
          return loc.room?.id === roomId && !loc.furniture && !loc.container;
        }
        return false;
      });
      return filtered;
    } catch (error) {
      console.error('Error fetching objects:', error);
      return [];
    } finally {
      setLoading(false);
    }
  };

  const updateCurrentItems = async (allHouses: House[], currentBreadcrumbs: Breadcrumb[]) => {
    if (currentBreadcrumbs.length === 0) {
      setCurrentItems(allHouses);
      setViewType('HOUSES');
      return;
    }

    const last = currentBreadcrumbs[currentBreadcrumbs.length - 1];
    
    if (last.type === 'HOUSES') {
      const house = allHouses.find(h => h.id === last.id);
      setCurrentItems(house?.rooms || []);
      setViewType('ROOMS');
    } else if (last.type === 'ROOMS') {
      const houseBreadcrumb = currentBreadcrumbs.find(b => b.type === 'HOUSES');
      const house = allHouses.find(h => h.id === houseBreadcrumb?.id);
      const room = house?.rooms.find(r => r.id === last.id);
      
      const furniture = room?.furniture || [];
      const roomObjects = await fetchObjects({ roomId: last.id });
      
      // Map objects to a common format for the list
      const objectItems = roomObjects.map((obj: any) => ({
        ...obj,
        isObject: true
      }));
      
      setCurrentItems([...furniture, ...objectItems]);
      setViewType('FURNITURE');
    } else if (last.type === 'FURNITURE') {
      const roomBreadcrumb = currentBreadcrumbs.find(b => b.type === 'ROOMS');
      const houseBreadcrumb = currentBreadcrumbs.find(b => b.type === 'HOUSES');
      const house = allHouses.find(h => h.id === houseBreadcrumb?.id);
      const room = house?.rooms.find(r => r.id === roomBreadcrumb?.id);
      const furniture = room?.furniture.find(f => f.id === last.id);
      
      const containers = furniture?.containers || [];
      const furnitureObjects = await fetchObjects({ furnitureId: last.id });
      
      const objectItems = furnitureObjects.map((obj: any) => ({
        ...obj,
        isObject: true
      }));
      
      setCurrentItems([...containers, ...objectItems]);
      setViewType('CONTAINERS');
    } else if (last.type === 'CONTAINERS') {
      const containerObjects = await fetchObjects({ containerId: last.id });
      const objectItems = containerObjects.map((obj: any) => ({
        ...obj,
        isObject: true
      }));
      setCurrentItems(objectItems);
      setViewType('OBJECTS');
    }
  };

  const handlePress = (item: any) => {
    const newBreadcrumb: Breadcrumb = {
      type: viewType,
      id: item.id,
      name: item.name
    };
    
    const newBreadcrumbs = [...breadcrumbs, newBreadcrumb];
    setBreadcrumbs(newBreadcrumbs);
    updateCurrentItems(houses, newBreadcrumbs);
  };

  const navigateBack = () => {
    const newBreadcrumbs = [...breadcrumbs];
    newBreadcrumbs.pop();
    setBreadcrumbs(newBreadcrumbs);
    updateCurrentItems(houses, newBreadcrumbs);
  };

  const handleBreadcrumbPress = (index: number) => {
    const newBreadcrumbs = breadcrumbs.slice(0, index);
    setBreadcrumbs(newBreadcrumbs);
    updateCurrentItems(houses, newBreadcrumbs);
  };

  const handleLogout = () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Logout', style: 'destructive', onPress: () => logout() }
    ]);
  };

  useEffect(() => {
    fetchHouses();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    fetchHouses();
  };

  const renderItem = ({ item }: { item: any }) => {
    let Icon = Building2;
    const isObject = item.isObject || viewType === 'OBJECTS';

    if (isObject) {
      Icon = Package;
    } else {
      if (viewType === 'ROOMS') Icon = Home;
      if (viewType === 'FURNITURE') Icon = Smartphone;
      if (viewType === 'CONTAINERS') Icon = Box;
    }

    return (
      <TouchableOpacity 
        style={styles.houseCard}
        onPress={() => isObject
          ? navigation.navigate('ObjectDetail', { object: item })
          : handlePress(item)}
      >
        <View style={styles.houseIcon}>
          <Icon size={24} color={isObject ? "#34C759" : "#007AFF"} />
        </View>
        <View style={styles.houseInfo}>
          <Text style={styles.houseName}>{item.name}</Text>
          {item.description && <Text style={styles.houseDesc}>{item.description}</Text>}
          {item.category && <Text style={styles.houseDesc}>{item.category}</Text>}
        </View>
        <ChevronRight size={20} color="#ccc" />
      </TouchableOpacity>
    );
  };

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.headerTitle}>Locations</Text>
          <View style={styles.breadcrumbContainer}>
            <TouchableOpacity onPress={() => handleBreadcrumbPress(0)}>
              <Text style={styles.breadcrumbText}>Root</Text>
            </TouchableOpacity>
            {breadcrumbs.map((b, i) => (
              <React.Fragment key={`${b.type}-${b.id}`}>
                <Text style={styles.breadcrumbSeparator}> / </Text>
                <TouchableOpacity onPress={() => handleBreadcrumbPress(i + 1)}>
                  <Text style={styles.breadcrumbText} numberOfLines={1}>{b.name}</Text>
                </TouchableOpacity>
              </React.Fragment>
            ))}
          </View>
        </View>
        <TouchableOpacity onPress={handleLogout} style={styles.logoutButton}>
          <LogOut size={20} color="#FF3B30" />
        </TouchableOpacity>
      </View>

      {loading && !refreshing ? (
        <ActivityIndicator style={styles.loader} size="large" color="#007AFF" />
      ) : (
        <FlatList
          data={currentItems}
          keyExtractor={(item) => `${viewType}-${item.id}`}
          renderItem={renderItem}
          contentContainerStyle={styles.list}
          refreshing={refreshing}
          onRefresh={onRefresh}
          ListEmptyComponent={
            <View style={styles.emptyContainer}>
              <Text style={styles.emptyText}>No {viewType.toLowerCase()} found.</Text>
              {viewType === 'HOUSES' && (
                <Text style={styles.emptySubtext}>You can add a location to organize your rooms and belongings.</Text>
              )}
            </View>
          }
        />
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#f8f9fa' },
  header: { 
    flexDirection: 'row', 
    justifyContent: 'space-between', 
    alignItems: 'flex-start', 
    paddingHorizontal: 20, 
    paddingTop: 60, 
    paddingBottom: 15,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#eee'
  },
  headerTitle: { fontSize: 24, fontWeight: '700', color: '#333' },
  breadcrumbContainer: { flexDirection: 'row', marginTop: 4, flexWrap: 'wrap', alignItems: 'center' },
  breadcrumbText: { fontSize: 14, color: '#007AFF' },
  breadcrumbSeparator: { fontSize: 14, color: '#999', marginHorizontal: 2 },
  logoutButton: { padding: 8 },
  list: { padding: 15 },
  houseCard: { 
    flexDirection: 'row', 
    alignItems: 'center', 
    backgroundColor: '#fff', 
    padding: 15, 
    borderRadius: 12, 
    marginBottom: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.05,
    shadowRadius: 3,
    elevation: 1
  },
  houseIcon: { 
    width: 48, 
    height: 48, 
    borderRadius: 24, 
    backgroundColor: '#F0F7FF', 
    justifyContent: 'center', 
    alignItems: 'center',
    marginRight: 15
  },
  houseInfo: { flex: 1 },
  houseName: { fontSize: 18, fontWeight: '600', color: '#333' },
  houseDesc: { fontSize: 14, color: '#666', marginTop: 2 },
  loader: { marginTop: 50 },
  emptyContainer: { alignItems: 'center', marginTop: 100, paddingHorizontal: 40 },
  emptyText: { fontSize: 18, fontWeight: '600', color: '#333', marginBottom: 10 },
  emptySubtext: { textAlign: 'center', color: '#999', lineHeight: 20 }
});
